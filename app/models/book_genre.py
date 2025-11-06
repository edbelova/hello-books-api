from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db

class BookGenre(db.Model):
    __tablename__ = "book_genre"
    genre_id: Mapped[int] = mapped_column(ForeignKey("genre.id"), primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), primary_key=True)
    genres: Mapped[list["Genre"]] = relationship(secondary="book_genre", back_populates="books")
    books: Mapped[list["Book"]] = relationship(secondary="book_genre", back_populates="genres") 