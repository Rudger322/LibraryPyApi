from datetime import date
from typing import Optional, List
from pydantic import BaseModel, field_validator
from typing import Generic, TypeVar
from typing import List, Generic, TypeVar
from pydantic import BaseModel

from app.books.schemas.author import AuthorBase, AuthorShort, AuthorDetail


class BookBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    first_publish_date: Optional[date] = None
    description: Optional[str] = None


class BookCreate(BookBase):
    authors_ids: Optional[List[int]] = []
    subjects: Optional[List[str]] = []
    cover_urls: Optional[List[str]] = []

    @field_validator('cover_urls')
    @classmethod
    def validate_urls(cls, v):
        if v:
            for url in v:
                if not url.startswith(('http://', 'https://')):
                    raise ValueError(f'Invalid URL: {url}. Must start with http:// or https://')
        return v


class BookDetails(BookBase):
    id: int
    authors: Optional[List[AuthorDetail]] = []
    subjects: Optional[List[str]] = []
    cover_urls: Optional[List[str]] = []

    model_config = {"from_attributes": True}


class BookShort(BaseModel):
    id: int
    title: str
    authors: Optional[List[AuthorShort]] = None
    cover_urls: Optional[List[str]] = []

    model_config = {"from_attributes": True}
class BookRead(BookBase):
    id: int
    cover_urls: Optional[List[str]] = []

    class Config:
        from_attributes = True

T = TypeVar('T')

class PaginatedResponse(BaseModel):
    """Пагинированный ответ"""
    total: int  # Общее количество записей
    page: int  # Текущая страница
    page_size: int  # Размер страницы
    items: List  # Список элементов (без Generic)

    model_config = {"from_attributes": True}