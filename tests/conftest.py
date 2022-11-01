import pytest
from app import create_app
from app import db
from flask.signals import request_finished


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    #function below will be invoked after any request
    #is completed
    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        #creates a new database session so that we can
        #test that changes were persisted in the database
        db.session.remove()

    #lets various functionality in Flask determine what
    #the current running app is
    with app.app_context():
        db.create_all()
        yield app

    #drop all of the tables, deleting any data that was
    #created during the test
    with app.app_context():
        db.drop_all()

#make a test client that will simulate making HTTP requests
@pytest.fixture
def client(app):
    return app.test_client()