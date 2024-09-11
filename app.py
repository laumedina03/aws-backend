from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow all origins for testing
# Database connection setup
def get_db_connection():
    return mysql.connector.connect(
        host='172.31.27.224',  # Replace with your MySQL server's private IP
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

if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=True)

