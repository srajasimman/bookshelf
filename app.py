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
def get_books():
    """
    Retrieves all books from the database and constructs a list of dictionaries with book information.
    No parameters are required. Returns a JSON response containing the list of books.
    """
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre}
        output.append(book_data)
    return jsonify({'books': output})

@app.route('/book/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """
    Retrieves a book from the database based on the provided book_id. Returns a JSON response containing the book's id, title, author, and genre.
    """
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre})

@app.route('/book/rnd', methods=['GET'])
def get_random_book():
    """
    Retrieves a random book from the database. Returns a JSON response containing the book's id, title, author, and genre.
    """
    book = Book.query.order_by(db.func.random()).first()
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre})

@app.route('/book', methods=['POST'])
def add_book():
    """
    A function to add a new book to the database.
    Retrieves book information from the request JSON, creates a new Book object, adds it to the database session, and commits the changes.
    Returns a JSON response with a message indicating the successful addition of the book.
    """
    data = request.json
    new_book = Book(title=data['title'], author=data['author'], genre=data.get('genre'))
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully!'})

@app.route('/books', methods=['POST'])
def add_books():
    """
    A function to add array of books to the database.
    Retrieves book information from the request JSON, creates a list of new Book objects, adds them to the database session, and commits the changes.
    Returns a JSON response with a message indicating the successful addition of the books.
    """
    data = request.json
    new_books = [Book(title=book['title'], author=book['author'], genre=book.get('genre')) for book in data]
    db.session.add_all(new_books)
    db.session.commit()
    return jsonify({'message': 'Books added successfully!'})
    

@app.route('/book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """
    Updates a book in the database with the provided book_id.
    
    Parameters:
        book_id (int): The unique identifier of the book to be updated.

    Returns:
        dict: A JSON response indicating the success of the update operation.
    """
    book = Book.query.get_or_404(book_id)
    data = request.json
    book.title = data['title']
    book.author = data['author']
    book.genre = data.get('genre')
    db.session.commit()
    return jsonify({'message': 'Book updated successfully!'})

@app.route('/book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """
    Deletes a book from the database using the provided book_id.
    
    Parameters:
        book_id (int): The unique identifier of the book to be deleted.

    Returns:
        dict: A JSON response indicating the success of the deletion operation.
    """
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
