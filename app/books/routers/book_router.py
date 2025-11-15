from fastapi import APIRouter, Depends
from typing import List, Optional

from app.books.schemas.cover import CoverRead, CoverCreate
from app.books.schemas.subject import SubjectRead, SubjectCreate
from app.books.services.book_service import BookService
from app.books.models.book import Book
from app.database.db import get_session, AsyncSession
from app.books.models.DTO.book_short import BookShortDTO
from app.books.schemas.book import BookRead, BookCreate, BookShort, BookDetails

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookRead)
async def create_book(data: BookCreate, session: AsyncSession = Depends(get_session)):
    return await BookService.add_book(session, data)

@router.get("/", response_model=List[BookShort])
async def get_short_books(session: AsyncSession = Depends(get_session)):
    return await BookService.get_short_books(session)

@router.get("/search", response_model=List[BookRead])
async def search_books(session: AsyncSession = Depends(get_session),
                       title_substring: str | None = None,
                       author_substring: str | None = None,
                       subject_substring: str | None = None):
    return await BookService.search_books(title_substring, author_substring, subject_substring, session)

#TODO: сделать
@router.get("/{id}", response_model=BookDetails)
async def get_book_details(id: int, session: AsyncSession = Depends(get_session)):
    return await BookService.get_book_details(id, session)

#TODO: проверить как работает

@router.post("/cover/", response_model=CoverRead)
async def create_cover_book(data: CoverCreate, session: AsyncSession = Depends(get_session)):
    return await BookService.add_cover_book(data, session)

@router.post("/subject/", response_model=SubjectRead)
async def create_subject_book(data: SubjectCreate, session: AsyncSession = Depends(get_session)):
    return await BookService.add_subject_book(data, session)