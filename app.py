from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
import requests

app = Flask(_name_)
CORS(app, resources={r"/*": {"origins": "http://ec2-3-218-165-24.compute-1.amazonaws.com:3000"}})  # Allow all origins for testing
# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host='ec2-100-28-15-106.compute-1.amazonaws.com',  # Replace with your MySQL server's private IP
        user='camilin',            # Replace with your MySQL username
        password='1234',    # Replace with your MySQL password
        database='mysql_parcial'      # Replace with your database name
    )

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

@app.route('/add-user',methods=['POST'])
def add_user():
    data = request.get_json()
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    birth_date = data.get('birth_date')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user (first_name, last_name, birth_date, password)
        VALUES (%s, %s, %s, %s)
    ''', (first_name, last_name, birth_date, password))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({'message': 'User added successfully!'}), 201

# Function to test POST request for adding user
"""def test_add_user():
    url = 'http://ec2-54-158-25-160.compute-1.amazonaws.com:5000/add-user'
    payload = {
        "first_name": "Test",
        "last_name": "Name",
        "birth_date": "1990-01-01",
        "password": "testpassword"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Test passed: User added successfully")
    else:
        print(f"Test failed: Status code {response.status_code}")"""



if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)
