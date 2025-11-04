from flask import Blueprint, make_response, request, Response
from app.models.book import Book
from ..models.author import Author
from .route_utilities import validate_model, handle_error, create_model
from ..db import db

bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

@bp.post("")
def create_author():
    request_body = request.get_json()
    return create_model(Author, request_body)

@bp.put("/<author_id>")
def update_author(author_id):
    author = validate_model(Author, author_id)
    request_body = request.get_json()

    author.name = request_body["name"]

    db.session.add(author)
    db.session.commit()

    return make_response(author.to_dict(), 200, {"Content-Type": "application/json"})

@bp.get("")
def get_all_authors():
    query = db.select(Author)

    name_param = request.args.get("name")
    if name_param:
        query = query.where(Author.name.ilike(f"%{name_param}%"))

    authors = db.session.scalars(query.order_by(Author.id))

    return [author.to_dict() for author in authors]

@bp.get("/<author_id>")
def get_one_author(author_id):
    author = validate_model(Author, author_id)
    return author.to_dict()

@bp.delete("/<author_id>")
def delete_author(author_id):
    author = validate_model(Author, author_id)
    db.session.delete(author)
    db.session.commit()
    return Response(status=204, mimetype="application/json")

@bp.post("/<author_id>/books")
def create_book_with_author(author_id):
    author = validate_model(Author, author_id)
    
    request_body = request.get_json()
    request_body["author_id"] = author.id

    return create_model(Book, request_body)

@bp.get("/<author_id>/books")
def get_books_by_author(author_id):
    author = validate_model(Author, author_id)
    return [book.to_dict() for book in author.books]