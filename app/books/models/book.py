from datetime import date
from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.books.models.book_author import book_authors_table
from app.database.db import Base

class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(500))
    subtitle: Mapped[Optional[str]] = mapped_column(String(500))
    first_publish_date: Mapped[Optional[date]] = mapped_column()
    description: Mapped[Optional[str]] = mapped_column(String(500))

    subjects: Mapped[Optional[List["BookSubject"]]] = relationship("BookSubject", back_populates="book", lazy="selectin")
    covers: Mapped[Optional[List["BookCover"]]] = relationship("BookCover", back_populates="book", lazy="selectin")
    authors: Mapped[Optional[List["Author"]]] = relationship(
            secondary=book_authors_table,
            back_populates="books", lazy="selectin"
        )
