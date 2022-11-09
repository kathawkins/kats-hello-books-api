from app import db
from flask import abort, make_response
from app.models.author import Author

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id")) #author is the table name in the DB
    author = db.relationship("Author", back_populates="books")

    def to_dict(self):
        book_as_dict = {}
        if not self.author_id:
            book_as_dict["id"] = self.id
            book_as_dict["title"] = self.title
            book_as_dict["description"] = self.description
        else:
            book_as_dict["id"] = self.id
            book_as_dict["title"] = self.title
            book_as_dict["description"] = self.description
            book_as_dict["author_id"] = self.author_id

        return book_as_dict

    @classmethod
    def from_json(cls, book_req_body, author_query = None):
        new_book = Book(title=book_req_body["title"],
                        description=book_req_body["description"],
                        author = author_query) #or author_id = author_query.id?
        return new_book

    def update(self, req_body):
        try:
            self.title = req_body["title"]
            self.description = req_body["description"]
        except KeyError as error:
            abort(make_response({"message": f"Missing attribute: {error}"}, 400))