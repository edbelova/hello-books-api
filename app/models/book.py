from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import Optional
from ..db import db

class Book(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[Optional[int]] = mapped_column(ForeignKey("author.id"))
    author: Mapped[Optional["Author"]] = relationship(back_populates="books")

    @classmethod
    def from_dict(cls, book_data):
        author_id = book_data.get("author_id")
        
        return cls(title=book_data["title"],
                   description=book_data["description"],
                   author_id=author_id)

    def to_dict(self):
        book_as_dict = {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
        if self.author:
            book_as_dict["author"] = self.author.to_dict()

        return book_as_dict