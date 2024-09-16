import unittest
from app import app  # Importa la aplicación Flask

class TestUserRegistration(unittest.TestCase):

    def setUp(self):
        # Configurar un cliente de prueba para interactuar con la app Flask
        self.app = app.test_client()
        self.app.testing = True

    def test_register_user(self):
        # Datos de prueba
        new_user = {
            'first_name': 'Juan',
            'last_name': 'Perez',
            'birth_date': '1990-01-01',
            'password': 'segura123'
        }
        response = self.app.post('/add-user', json=new_user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User added successfully!', str(response.data))

if __name__ == '__main__':
    unittest.main()
