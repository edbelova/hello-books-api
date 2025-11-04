from flask import Blueprint, make_response, request, Response

from ..models.author import Author
from ..models.book import Book
from .route_utilities import create_model, get_models_with_filters, validate_model
from ..db import db

bp = Blueprint("books_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()
    return create_model(Book, request_body)

@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    if book.author_id:
        author = validate_model(Author, book.author_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]
    book.author_id = request_body.get("author_id", book.author_id)

    db.session.commit()

    return make_response(book.to_dict(), 200, {"Content-Type": "application/json"})

@bp.get("")
def get_all_books():
    return get_models_with_filters(Book, request.args)

@bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_model(Book, book_id)
    return book.to_dict()

@bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_model(Book, book_id)
    db.session.delete(book)
    db.session.commit()
    return Response(status=204, mimetype="application/json")