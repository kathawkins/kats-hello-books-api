from app import db
from flask import abort, make_response

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"))
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
    def from_json(cls, book_req_body):
        if "author_id" in book_req_body:
            new_book = Book(title=book_req_body["title"],
                        description=book_req_body["description"],
                        author_id = book_req_body["author_id"])
        else:
            new_book = Book(title=book_req_body["title"],
                        description=book_req_body["description"])
            # does the same as:
            # new_book = cls(title=book_req_body["title"],
            #             description=book_req_body["description"])
        return new_book

    def update(self, req_body):
        try:
            self.title = req_body["title"]
            self.description = req_body["description"]
        except KeyError as error:
            abort(make_response({"message": f"Missing attribute: {error}"}, 400))