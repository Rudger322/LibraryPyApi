from fastapi import APIRouter, Depends
from typing import List, Optional

from starlette import status

from app.auth.utils.dependencies import get_current_admin_user
from app.books.schemas.cover import CoverRead, CoverCreate
from app.books.schemas.subject import SubjectRead, SubjectCreate
from app.books.services.book_service import BookService
from app.books.models.book import Book
from app.database.db import get_session, AsyncSession
from app.books.models.DTO.book_short import BookShortDTO
from app.books.schemas.book import BookRead, BookCreate, BookShort, BookDetails
from fastapi import APIRouter, Depends, UploadFile, File, Request
from fastapi.responses import FileResponse
from app.books.schemas.cover import CoverRead
from fastapi import HTTPException
from app.auth.utils.dependencies import get_current_admin_user
from app.auth.models.user import User

router = APIRouter(prefix="/books", tags=["books"])

@router.post("/", response_model=BookRead)
async def create_book(data: BookCreate, session: AsyncSession = Depends(get_session)):
    return await BookService.add_book(session, data)

@router.get("/", response_model=List[BookShort])
async def get_short_books(session: AsyncSession = Depends(get_session),
                       title_substring: str | None = None,
                       author_substring: str | None = None,
                       subject_substring: str | None = None):
    return await BookService.get_short_books(title_substring, author_substring, subject_substring, session)

@router.get("/{id}", response_model=BookDetails)
async def get_book_details(
    id: int,
    request: Request,  # Добавили
    session: AsyncSession = Depends(get_session)
):
    """Получить детали книги с URL обложек"""
    book = await BookService.get_book_details(id, session, request)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/subject/", response_model=SubjectRead)
async def create_subject_book(data: SubjectCreate, session: AsyncSession = Depends(get_session)):
    return await BookService.add_subject_book(data, session)


@router.post("/{book_id}/covers/upload", response_model=CoverRead)
async def upload_book_cover(
        book_id: int,
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    """
    Загрузить обложку для книги (только для библиотекарей)

    Принимает изображение (JPG, PNG, WEBP, GIF) размером до 5 МБ
    """
    return await BookService.upload_cover(session, book_id, file)


@router.get("/covers/{cover_id}")
async def get_book_cover(
        cover_id: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Получить изображение обложки по ID

    Возвращает файл изображения
    """
    file_path = await BookService.get_cover_file(session, cover_id)
    return FileResponse(file_path)


@router.delete("/covers/{cover_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_cover(
        cover_id: int,
        session: AsyncSession = Depends(get_session)
):
    """
    Удалить обложку книги (только для библиотекарей)
    """
    await BookService.delete_cover(session, cover_id)