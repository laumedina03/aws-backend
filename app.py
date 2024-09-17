from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://ec2-3-218-165-24.compute-1.amazonaws.com:3000"}})  # Allow all origins for testing

# Database connection setup
def get_db_connection():
    if os.getenv('FLASK_ENV') == 'testing':
        # Use SQLite in-memory for testing
        conn = sqlite3.connect(':memory:')
        create_table_if_not_exists(conn)  # Create the table when connecting
        return conn
    else:
        conn = mysql.connector.connect(
            host='ec2-100-28-15-106.compute-1.amazonaws.com',  # Replace with your MySQL server's private IP
            user='camilin',            # Replace with your MySQL username
            password='1234',    # Replace with your MySQL password
            database='mysql_parcial'      # Replace with your database name
        )
        return conn

def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS table1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            birth_date TEXT,
            password TEXT
        )  
    ''')
    conn.commit()
    cursor.close()
    
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/data')
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM user')  # Replace with your table name
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birth_date = data.get('birth_date')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    # Use different placeholders for SQLite and MySQL
    if os.getenv('FLASK_ENV') == 'testing':
        query = 'INSERT INTO user (first_name, last_name, birth_date, password) VALUES (?, ?, ?, ?)'
    else:
        query = 'INSERT INTO user (first_name, last_name, birth_date, password) VALUES (%s, %s, %s, %s)'

    try:
        cursor.execute(query, (first_name, last_name, birth_date, password))
        conn.commit()
        return jsonify({'message': 'User added successfully!'})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'message': 'Failed to add user'}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)

