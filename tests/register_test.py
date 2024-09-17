import unittest
import os
import sqlite3
from app import app

class RegisterUserTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
	"""Set up a temporary in-memory database."""
	cls.app = app
	cls.app.config['TESTING'] = True
	cls.app.config['DATABASE'] = ':memory:'
	cls.client = cls.app.test_client()

	with cls.app.app_context():
	    conn = sqlite3.connect(':memory:')
	    cursor = conn.cursor()
            cursor.execute('''
		CREATE TABLE IF NOT EXISTS user (
		    id INTEGER PRIMARY KEY AUTOINCREMENT,
		    first_name TEXT NOT NULL,
	            last_name TEXT NOT NULL,
		    birth_date TEXT NOT NULL,
	            password TEXT NOT NULL
	         )
	     ''')
	     conn.commit()
	     conn.close()

    def setUp(self):
        """Set up the database connection for each test."""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.app.config['DATABASE'] = ':memory:'

    def tearDown(self):
        """Clean up after each test."""
        self.conn.close()

    def test_register_user(self):
        response = self.client.post('/add_user', json={
            "first_name": "John",
            "last_name": "Doe",
            "birth_date": "1990-01-01",
            "password": "password123"
        })                           
        self.assertEqual(response.status_code, 201)

    def test_get_users(self):
        response = self.client.get('/data')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
