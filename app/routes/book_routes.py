from flask import Blueprint, make_response, request, Response
from ..models.book import Book
from .route_utilities import validate_model, handle_error
from ..db import db

bp = Blueprint("books_bp", __name__, url_prefix="/books")

@bp.post("")
def create_book():
    request_body = request.get_json()

    try:
        new_book = Book.from_dict(request_body)
    except KeyError as error:
        handle_error(f"Invalid request: missing {error.args[0]}", 400)

    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201

@bp.put("/<book_id>")
def update_book(book_id):
    book = validate_model(Book, book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(book.to_dict(), 200, {"Content-Type": "application/json"})

@bp.get("")
def get_all_books():
    query = db.select(Book)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Book.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Book.description.ilike(f"%{description_param}%"))

    min_param = request.args.get("min")
    if min_param:
        query = query.where(Book.id >= int(min_param))
    
    max_param = request.args.get("max")
    if max_param:
        query = query.where(Book.id <= int(max_param))

    books = db.session.scalars(query.order_by(Book.id))

    return [book.to_dict() for book in books]

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