from app import db
from flask import abort, make_response

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)

    @classmethod
    def from_json(cls, genre_req_body):
        new_genre = Genre(name=genre_req_body["name"])
        return new_genre

    def update(self, req_body):
        try:
            self.title = req_body["name"]
        except KeyError as error:
            abort(make_response({"message": f"Missing attribute: {error}"}, 400))

    def to_dict(self):
        dict = {"name": self.name}
        return dict