from flask import Flask, jsonify
import psycopg2

try:
    connection = psycopg2.connect(
        dbname='book_store', 
        user='postgres',
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
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM authors;")
        results = cursor.fetchall()
        authors = []
        for result in results:
            author = {
                'id': result[0],
                'name': result[1],
                'age': result[2],
                'created_at': result[3]
            }
            authors.append(author)
        return jsonify({'authors': authors})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/books')
def books():    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        results = cursor.fetchall()
        books = []
        for result in results:
            book = {
                'id': result[0],
                'isbn': result[1],
                'name': result[2],
                'cant_pages': result[3],
                'created_at': result[4],
                'author': result[5]
            }
            books.append(book)
        return jsonify({'books': books})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)