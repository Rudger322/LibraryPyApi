from typing import List
from pydantic import BaseModel
from app.books.schemas.book import BookShort

class ShowcaseUpdate(BaseModel):
    book_ids: List[int]

class ShowcaseResponse(BaseModel):
    total: int
    books: List[BookShort]