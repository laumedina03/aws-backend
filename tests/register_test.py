import unittest
import json
import os
from app import app, get_db_connection, get_table_name

class RegisterUserTestCase(unittest.TestCase):

    def setUp(self):
        """Configuración inicial, ejecutada antes de cada prueba."""
        app.config['TESTING'] = True
        os.environ['FLASK_ENV'] = 'testing'
        self.app = app.test_client()
        self.conn = get_db_connection(test_db=True)  # Use SQLite in-memory database
        self.create_tables()

    def create_tables(self):
        """Crea las tablas necesarias para las pruebas."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_test (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                birth_date TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def test_register_user(self):
        """Prueba para registrar un usuario."""
        response = self.app.post('/add-user',
                                 data=json.dumps({
                                     "first_name": "John",
                                     "last_name": "Doe",
                                     "birth_date": "1990-01-01",
                                     "password": "password123"
                                 }),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # JAJAJA Verifica que el usuario fue insertado en la base de datos
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM user_test WHERE first_name=?', ('John',))
        user = cursor.fetchone()
        print("User retrieved from test database:", user)  # Debugging line
        self.assertIsNotNone(user)
        self.assertEqual(user['last_name'], 'Doe')  # Verifica el apellido

    def tearDown(self):
        """Limpia después de cada prueba."""
        cursor = self.conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS user_test')
        self.conn.commit()
        self.conn.close()

if __name__ == '__main__':
    unittest.main()
