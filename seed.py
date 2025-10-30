from app import create_app, db
from app.models.book import Book

my_app = create_app()
with my_app.app_context():
    books = [
        Book(title="Fictional Book", description="A fantasy novel set in an imaginary world."),
        Book(title="Wheel of Time", description="A fantasy novel set in an imaginary world."),
        Book(title="Fictional Book Title", description="A fantasy novel set in an imaginary world.")
    ]
    db.session.add_all(books)
    db.session.commit()
