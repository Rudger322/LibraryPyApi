from sqlmodel import SQLModel, Field

class BookAuthor(SQLModel, table=True):
    book_key: str = Field(foreign_key="book.key", primary_key=True)
    author_key: str = Field(foreign_key="author.key", primary_key=True)
