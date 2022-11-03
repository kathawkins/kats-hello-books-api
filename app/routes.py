from app import db
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, jsonify, abort, make_response, request

books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

"""
AUTHORS
"""
@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author.from_json(request_body)

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)

@authors_bp.route("", methods=["GET"])
def read_all_authors():
    name_query = request.args.get("name")
    if name_query:
        authors = Author.query.filter_by(title=name_query)
    else:
        authors = Author.query.all()

    return jsonify([author.to_dict() for author in authors])

@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)

    request_body = request.get_json()
    new_book = Book(title=request_body["title"],
                    description=request_body["description"],
                    author_id = author.id) #Learn lesson had author = author (???)
    # new_book = Book.from_json(request_body)

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

@authors_bp.route("/<author_id>/books", methods=["GET"])
def read_books_from_author(author_id):
    author = validate_model(Author, author_id)
    return jsonify([book.to_dict() for book in author.books])

"""
BOOKS
"""
@books_bp.route("", methods=["POST"])
def create_book_record():
    request_body = request.get_json()
    new_book = Book.from_json(request_body)

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)

@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    return jsonify([book.to_dict() for book in books]) 

def validate_model(cls, id):
    try:
        model_id = int(id)
    except:
        abort(make_response({"message":f"{cls.__name__} {id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {id} not found"}, 404))

    return model

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_model(Book, book_id)
    return book.to_dict()

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_model(Book, book_id)

    request_body = request.get_json()

    book.update(request_body)

    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully updated"))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"))