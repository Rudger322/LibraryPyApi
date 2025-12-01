from typing import List, Optional
from app.books.models.book import Book
from app.books.repositories.book_repository import BookRepository
from app.books.schemas.book import BookCreate, BookRead, BookShort, BookDetails
from app.books.schemas.cover import CoverCreate, CoverRead
from app.books.schemas.subject import SubjectCreate
from app.database.db import AsyncSession
from app.books.schemas.cover import CoverURL
import os
import uuid
from fastapi import UploadFile, HTTPException, status
from app.config.conf import UPLOAD_DIR, ALLOWED_EXTENSIONS, MAX_FILE_SIZE

class BookService:

    @staticmethod
    async def add_book(session: AsyncSession, data: BookCreate) -> BookRead:
        book = Book(
            title=data.title,
            subtitle=data.subtitle,
            first_publish_date=data.first_publish_date,
            description=data.description
        )

        book = await BookRepository.add_book(
            session,
            book,
            authors_ids=data.authors_ids or [],
            subjects=data.subjects or [],
            covers=[]
        )

        return BookRead.model_validate(book)

    @staticmethod
    async def get_short_books(title_substring: str,
                           author_substring: str,
                           subject_substring: str,
                           session: AsyncSession) -> List[BookShort]:

        if title_substring is not None:
            title_books = await BookRepository.get_books_by_title(title_substring, session)
        else:
            title_books = await BookRepository.get_books(session)

        if author_substring is not None:
            author_books = await BookRepository.get_books_by_author(author_substring, session)
        else:
            author_books = await BookRepository.get_books(session)

        if subject_substring is not None:
            subject_books = await BookRepository.get_books_by_subject(subject_substring, session)
        else:
            subject_books = await BookRepository.get_books(session)

        title_ids = {book.id for book in title_books}
        author_ids = {book.id for book in author_books}
        subject_ids = {book.id for book in subject_books}

        final_ids = title_ids & author_ids & subject_ids

        final_books = [BookShort.model_validate(book) for book in title_books if book.id in final_ids]

        return final_books

    @staticmethod
    async def get_book_details(id: int, session: AsyncSession, request) -> BookDetails | None:
        """Получить детали книги с URL обложек"""
        book = await BookRepository.get_book_details(id, session)

        if not book:
            return None

        # Формируем URL для обложек
        base_url = str(request.base_url).rstrip('/')
        covers = [
            CoverURL(
                id=cover.id,
                url=f"{base_url}/books/covers/{cover.id}"
            )
            for cover in book.covers
        ] if book.covers else []

        return BookDetails(
            id=book.id,
            title=book.title,
            subtitle=book.subtitle,
            first_publish_date=book.first_publish_date,
            description=book.description,
            authors=[a.name for a in book.authors] if book.authors else [],
            subjects=[s.subject for s in book.subjects] if book.subjects else [],
            covers=covers
        )

    @staticmethod
    async def add_subject_book(data: SubjectCreate, session: AsyncSession):
        return await BookRepository.add_subject_book(data, session)

    @staticmethod
    async def upload_cover(
            session: AsyncSession,
            book_id: int,
            file: UploadFile
    ) -> CoverRead:
        """Загрузить обложку для книги"""

        # Проверяем существование книги
        book = await BookRepository.get_book_details(book_id, session)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        # Проверяем расширение файла
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )

        # Читаем файл и проверяем размер
        contents = await file.read()
        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Max size: {MAX_FILE_SIZE / 1024 / 1024}MB"
            )

        # Генерируем уникальное имя файла
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        # Сохраняем файл
        with open(file_path, "wb") as f:
            f.write(contents)

        # Сохраняем путь в БД (относительный путь)
        cover = await BookRepository.add_cover(session, book_id, unique_filename)

        return CoverRead.model_validate(cover)

    @staticmethod
    async def get_cover_file(session: AsyncSession, cover_id: int) -> str:
        """Получить путь к файлу обложки"""
        cover = await BookRepository.get_cover_by_id(session, cover_id)
        if not cover:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cover not found"
            )

        file_path = os.path.join(UPLOAD_DIR, cover.cover_file)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cover file not found on server"
            )

        return file_path

    @staticmethod
    async def delete_cover(session: AsyncSession, cover_id: int) -> None:
        """Удалить обложку"""
        cover = await BookRepository.get_cover_by_id(session, cover_id)
        if not cover:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cover not found"
            )

        # Удаляем файл с диска
        file_path = os.path.join(UPLOAD_DIR, cover.cover_file)
        if os.path.exists(file_path):
            os.remove(file_path)

        # Удаляем запись из БД
        await BookRepository.delete_cover(session, cover)