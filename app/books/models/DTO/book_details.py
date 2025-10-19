from typing import Optional, List
from sqlmodel import SQLModel, Field
from app.books.models.DTO.author_short import AuthorShortDTO

class BookDetailsDTO(SQLModel):
    key: str
    title: str
    first_publish_year: Optional[int] = None
    description: Optional[str] = None
    authors: List[AuthorShortDTO] = []
    subjects: List[str] = []