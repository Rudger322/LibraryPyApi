from typing import List, Optional
from app.books.models.book import Book
from app.books.repositories.book_repository import BookRepository
from app.books.schemas.book import BookCreate, BookRead, BookShort, BookDetails
from app.books.schemas.cover import CoverCreate
from app.books.schemas.subject import SubjectCreate
from app.database.db import AsyncSession
from app.books.schemas.book import PaginatedResponse

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
            covers=data.covers or []
        )

        return BookRead.model_validate(book)


    @staticmethod
    async def get_short_books(
            session: AsyncSession,
            title_substring: str | None = None,
            author_substring: str | None = None,
            subject_substring: str | None = None,
            page: int = 1,
            page_size: int = 10
    ) -> PaginatedResponse:  # Убрали [BookShort]
        """
        Получить книги с фильтрацией и пагинацией

        Если указаны несколько фильтров, они работают по логике AND
        """
        # Используем новый универсальный метод с фильтрами
        books, total = await BookRepository.get_books_by_filters_paginated(
            session=session,
            title_substring=title_substring,
            author_substring=author_substring,
            subject_substring=subject_substring,
            page=page,
            page_size=page_size
        )

        # Конвертируем в BookShort
        book_shorts = [BookShort.model_validate(book) for book in books]

        return PaginatedResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=book_shorts
        )

    @staticmethod
    async def get_book_details(id: int, session: AsyncSession) -> BookDetails | None:
        return await BookRepository.get_book_details(id, session)

    @staticmethod
    async def add_cover_book(data: CoverCreate, session: AsyncSession):
        return await BookRepository.add_cover_book(data, session)

    @staticmethod
    async def add_subject_book(data: SubjectCreate, session: AsyncSession):
        return await BookRepository.add_subject_book(data, session)