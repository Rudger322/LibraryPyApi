from sqlalchemy import ForeignKey, Column, Table
from app.database.db import Base

book_authors_table = Table(
    "books_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True)
)