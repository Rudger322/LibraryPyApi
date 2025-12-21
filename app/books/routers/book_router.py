from fastapi import APIRouter, Depends
from typing import List, Optional

from app.books.schemas.cover import CoverRead, CoverCreate
from app.books.schemas.subject import SubjectRead, SubjectCreate
from app.books.services.book_service import BookService
from app.books.models.book import Book
from app.database.db import get_session, AsyncSession
from app.books.models.DTO.book_short import BookShortDTO
from app.books.schemas.book import BookRead, BookCreate, BookShort, BookDetails, PaginatedResponse

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookRead)
async def create_book(data: BookCreate, session: AsyncSession = Depends(get_session)):
    return await BookService.add_book(session, data)


@router.get("/")  # Убрали response_model отсюда
async def get_short_books(
        session: AsyncSession = Depends(get_session),
        title_substring: str | None = None,
        author_substring: str | None = None,
        subject_substring: str | None = None,
        page: int = 1,
        page_size: int = 10
) -> PaginatedResponse:  # Указали здесь
    """
    Получить список книг с фильтрацией и пагинацией

    Параметры:
    - title_substring: поиск по названию (опционально)
    - author_substring: поиск по автору (опционально)
    - subject_substring: поиск по теме (опционально)
    - page: номер страницы (по умолчанию 1)
    - page_size: количество элементов на странице (по умолчанию 10, макс 100)

    Фильтры работают по логике AND (все условия должны выполняться)
    """
    # Ограничиваем максимальный размер страницы
    if page_size > 100:
        page_size = 100

    if page < 1:
        page = 1

    return await BookService.get_short_books(
        session=session,
        title_substring=title_substring,
        author_substring=author_substring,
        subject_substring=subject_substring,
        page=page,
        page_size=page_size
    )

@router.get("/{id}", response_model=BookDetails)
async def get_book_details(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    book = await BookService.get_book_details(id, session)
    return book

@router.post("/subject/", response_model=SubjectRead)
async def create_subject_book(data: SubjectCreate, session: AsyncSession = Depends(get_session)):
    return await BookService.add_subject_book(data, session)