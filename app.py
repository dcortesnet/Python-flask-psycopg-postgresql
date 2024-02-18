from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
import atexit

try:
    connection = psycopg2.connect(
        dbname='book_store', 
        user='postgres',
        password='123456', 
        host='localhost',
        port=5432,
        cursor_factory=RealDictCursor
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
def get_authors():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM authors")
        results = cursor.fetchall()
        authors = []
        for result in results:
            author = {
                'author_id': result['author_id'],
                'name': result['name'],
                'age': result['age'],
                'created_at': result['created_at']
            }
            authors.append(author)
        return jsonify({'authors': authors})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/authors', methods=['POST'])
def create_author():
    try:
        data = request.json
        name = data.get('name')
        age = data.get('age')
        if not name or not age:
            return jsonify({'message': 'Bad request, name or age not found'}), 400
        cursor = connection.cursor()
        cursor.execute("INSERT INTO authors (name, age) VALUES (%s, %s) RETURNING author_id, name, age, created_at", (name, age))
        connection.commit()
        result = cursor.fetchone()
        author = {
            'author_id': result['author_id'],
            'name': result['name'],
            'age': result['age'],
            'created_at': result['created_at']
        }       
        return jsonify({'author': author}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/books')
def get_books():    
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM books")
        results = cursor.fetchall()
        books = []
        for result in results:
            book = {
                'book_id': result['book_id'],
                'isbn': result['isbn'],
                'name': result['name'],
                'cant_pages': result['cant_pages'],
                'created_at': result['created_at'],
                'author_id': result['author_id']
            }
            books.append(book)
        return jsonify({'books': books})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@app.route('/books', methods=['POST'])
def create_book():
    try:
        data = request.json
        isbn = data.get('isbn')
        name = data.get('name')
        cant_pages = data.get('cant_pages')
        author_id = data.get('author_id')
        if not name or not cant_pages or not author_id or not isbn:
            return jsonify({'message': 'Bad request, isbn or name or cantPages or author not found'}), 400
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO books (isbn, name, cant_pages, author_id) 
            VALUES (%s, %s, %s, %s) RETURNING book_id, isbn, name, cant_pages, author_id, created_at
            """, 
        (isbn, name, cant_pages, author_id))
        connection.commit()
        result = cursor.fetchone()
        book = {
            'book_id': result['book_id'],
            'isbn': result['isbn'],
            'name': result['name'],
            'cant_pages': result['cant_pages'],
            'author_id': result['author_id'],
            'created_at': result['created_at']
        }
        return jsonify({'book': book}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

def close_connection():
    if 'connection' in globals():
        connection.close()
        print('Connection to the database closed')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
    atexit.register(close_connection)
