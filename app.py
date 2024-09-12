import unittest
import os
from app import app, db, User  # Import the app, db, and User model

class TestUserRegistration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set the environment to testing
        os.environ['FLASK_ENV'] = 'testing'

    def setUp(self):
        # Configurar un cliente de prueba para interactuar con la app Flask
        self.app = app.test_client()
        self.app.testing = True

        # Set up the database for testing
        with app.app_context():
            db.create_all()
    
    def tearDown(self):
        # Clean up after each test
        with app.app_context():
            db.session.remove()
            db.drop_all()  # Drop all tables

    def test_register_user(self):
        # Datos de prueba
        new_user = {
            'first_name': 'Ana',
            'last_name': 'Gomez',
            'birth_date': '1992-05-12',
            'password': 'nueva123'
        }
        response = self.app.post('/add-user', json=new_user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added successfully!', str(response.data))

if __name__ == '__main__':
    unittest.main()

