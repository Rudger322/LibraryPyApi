from typing import Optional
from sqlmodel import SQLModel

class BookCreate(SQLModel):
    title: str
    author_name: str

class BookRead(SQLModel):
    id: int
    title: str
    author_name: str
