from flask import Blueprint, jsonify

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Fictional Book TitleA", "A fantasy novel set in an old imaginary world."),
    Book(2, "Fictional Book TitleB", "A fantasy novel set in a modern imaginary world."),
    Book(3, "Fictional Book TitleC", "A fantasy novel set in a futuristic imaginary world.")
] 

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods=["GET"])
def handle_books():
    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    # return books_response
    return jsonify(books_response)