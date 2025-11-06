import pytest
from app import create_app
from app.db import db
from app.models.author import Author
from app.models.book import Book
from flask.signals import request_finished
from dotenv import load_dotenv
import os

load_dotenv()

@pytest.fixture
def app():
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('SQLALCHEMY_TEST_DATABASE_URI')
    }
    app = create_app(test_config)

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_saved_books(app):
    ocean_book = Book(title="Ocean Book", description="watr 4evr")
    mountain_book = Book(title="Mountain Book", description="i luv 2 climb rocks")

    db.session.add_all([ocean_book, mountain_book])
    db.session.commit()

@pytest.fixture
def two_saved_authors(app):
    author1 = Author(name="Author One")
    author2 = Author(name="Author Two")

    db.session.add_all([author1, author2])
    db.session.commit()

@pytest.fixture
def two_saved_genres(app):
    from app.models.genre import Genre

    genre1 = Genre(name="Fantasy")
    genre2 = Genre(name="Science Fiction")

    db.session.add_all([genre1, genre2])
    db.session.commit()