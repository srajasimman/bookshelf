from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Book model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f'<Book {self.title}>'

# Create the database tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/books', methods=['GET'])
def list_books():
    """Retrieve all books."""
    books = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre
        }
        for book in Book.query.all()
    ]
    return jsonify({'books': books})

@app.route('/book/<int:book_id>', methods=['GET'])
def get_book_by_id(book_id):
    """Retrieves book by id."""
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre})

@app.route('/book/random', methods=['GET'])
def random_book():
    """Retrieves a random book from the database."""
    book = Book.query.order_by(db.func.random()).first()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre})

@app.route('/book/random/<int:count>', methods=['GET'])
def random_books(count):
    """Retrieves a random set of books from the database."""
    books = Book.query.order_by(db.func.random()).limit(count).all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre} for book in books])

@app.route('/book', methods=['POST'])
def add_book():
    """Adds a new book to the database."""
    book_data = request.get_json()
    book = Book(title=book_data['title'], author=book_data['author'], genre=book_data.get('genre'))
    db.session.add(book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully.'}), 201

@app.route('/books', methods=['POST'])
def add_books():
    books = [Book(title=book['title'], author=book['author'], genre=book.get('genre'))
             for book in request.json]
    db.session.add_all(books)
    db.session.commit()
    return jsonify({'message': 'Books added successfully!'}), 201

@app.route('/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Updates a book in the database"""
    book = Book.query.get_or_404(book_id)
    data = request.json
    book.title = data['title']
    book.author = data['author']
    book.genre = data.get('genre')
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

@app.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Deletes a book by id."""
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
