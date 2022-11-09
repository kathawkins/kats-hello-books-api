from app import db
# from flask import abort, make_response

class BookGenre(db.Model):
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), primary_key=True,nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True,nullable=False)