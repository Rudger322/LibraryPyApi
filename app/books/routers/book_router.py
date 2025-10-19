from fastapi import APIRouter, Depends
from typing import List, Optional
from sqlmodel import SQLModel

from app.books.models.DTO.book_details import BookDetailsDTO
from app.books.services.book_service import BookService
from app.books.models.book import Book
from app.database.db import get_session, AsyncSession

from app.books.models.DTO.book_short import BookShortDTO

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=Book)
async def create_book(key: str, title: str, author_key: str, session: AsyncSession = Depends(get_session)):
    return await BookService.add_book(session, key, title, author_key)

@router.get("/", response_model=List[Book])
async def list_books(session: AsyncSession = Depends(get_session)):
    return await BookService.get_books(session)

@router.get("/search", response_model=List[BookShortDTO])
async def get_all_books(session: AsyncSession = Depends(get_session),
                        title: Optional[str] = None,
                        author: Optional[str] = None,
                        subject: Optional[str] = None):
    return await BookService.get_all_books(session, title, author, subject)

@router.get("/search/{key}", response_model=BookDetailsDTO)
async def get_detail_book(key: str, session: AsyncSession = Depends(get_session)):
    return await BookService.get_book_details(session, key)