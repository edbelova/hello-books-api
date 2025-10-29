from app import create_app, db
from app.models.book import Book

my_app = create_app()
with my_app.app_context():
    book = Book(title="The Great Gatsby", description="A novel by F. Scott Fitzgerald")
    db.session.add(book)
    db.session.commit()