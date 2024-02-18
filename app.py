from flask import Flask, jsonify
import psycopg2

try:
    connection = psycopg2.connect(
        dbname='book_store', 
        user='postgress',
        password='123456', 
        host='localhost',
        port=5432
    )
    print('Successful connection to the database')
except Exception as error:
    print('Database connection error')

app = Flask(__name__)
port = 5000

@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/authors')
def authors():
    try:
        pass
        return jsonify({'authors': []})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/books')
def books():    
    try:
        pass
        return jsonify({'books': []})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)