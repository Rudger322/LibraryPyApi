from datetime import date
from typing import Optional, List
from pydantic import BaseModel

from app.books.schemas.author import AuthorBase, AuthorShort


class BookBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    first_publish_date: Optional[date] = None
    description: Optional[str] = None

class BookCreate(BookBase):
    authors_ids: Optional[List[int]] = []
    subjects: Optional[List[str]] = []
    covers: Optional[List[int]] = []

class BookDetails(BookBase):
    authors: Optional[List[str]] = []
    subjects: Optional[List[str]] = []
    covers: Optional[List[int]] = []
    model_config = {"from_attributes": True}

class BookShort(BaseModel):
    id: int
    title: str
    authors: Optional[List[AuthorShort]] = None
    model_config = {"from_attributes": True}

class BookRead(BookBase):
    id: int

    class Config:
        from_attributes = True