from fastapi import APIRouter, Depends
from typing import List
from sqlmodel import SQLModel
from app.books.services.book_service import BookService
from app.books.models.book import Book
from app.database.db import get_session, AsyncSession

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=Book)
async def create_book(key: str, title: str, author_key: str, session: AsyncSession = Depends(get_session)):
    return await BookService.add_book(session, key, title, author_key)

@router.get("/", response_model=List[Book])
async def list_books(session: AsyncSession = Depends(get_session)):
    return await BookService.get_books(session)
