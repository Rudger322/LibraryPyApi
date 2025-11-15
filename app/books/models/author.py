from datetime import date
from typing import Optional, List
from app.books.models.book_author import book_authors_table
from app.database.db import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Author(Base):
    __tablename__ = "authors"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    bio: Mapped[Optional[str]] = mapped_column(String(500))
    birth_date: Mapped[Optional[date]] = mapped_column()
    death_date: Mapped[Optional[date]] = mapped_column()
    wikipedia: Mapped[Optional[str]] = mapped_column(String(255))

    books: Mapped[List["Book"]] = relationship(
            secondary=book_authors_table,
            back_populates="authors"
    )