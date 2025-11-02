from flask import Blueprint, abort, make_response, request, Response
from ..models.book import Book
from ..db import db

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

@books_bp.post("")
def create_book():
    request_body = request.get_json()

    try:
        new_book = Book.from_dict(request_body)
    except KeyError as error:
        handle_error(f"Invalid request: missing {error.args[0]}", 400)

    db.session.add(new_book)
    db.session.commit()

    return new_book.to_dict(), 201

@books_bp.put("/<book_id>")
def update_book(book_id):
    book = validate_book(book_id)
    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(book.to_dict(), 200, {"Content-Type": "application/json"})

@books_bp.get("")
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

@books_bp.get("/<book_id>")
def get_one_book(book_id):
    book = validate_book(book_id)
    return book.to_dict()

@books_bp.delete("/<book_id>")
def delete_book(book_id):
    book = validate_book(book_id)
    db.session.delete(book)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        handle_error(f"book {book_id} invalid", 400)

    query = db.select(Book).where(Book.id == book_id)
    book = db.session.scalar(query)
    
    if not book:
        handle_error(f"book {book_id} not found", 404)
    return book

def handle_error(message, status_code):
    abort(make_response({"message": message}, status_code))

def apply_filtering(query):
    # This function is a placeholder for potential future filtering logic.
    return query