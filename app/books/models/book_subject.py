from sqlmodel import SQLModel, Field
from typing import Optional

class BookSubject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject: str = Field(max_length=400)
    book_key: str = Field(foreign_key="book.key")  
