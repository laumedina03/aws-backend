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
            'nombres': 'Juan',
            'apellidos': 'Perez',
            'fecha_nacimiento': '1990-01-01',
            'password': 'segura123'
        }
        response = self.app.post('/register', json=new_user)
        self.assertEqual(response.status_code, 201)
        self.assertIn('Usuario registrado exitosamente', str(response.data))

if __name__ == '__main__':
    unittest.main()
