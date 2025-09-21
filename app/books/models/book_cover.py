from sqlmodel import SQLModel, Field
from typing import Optional

class BookCover(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cover_file: int
    book_key: str = Field(foreign_key="book.key")  
