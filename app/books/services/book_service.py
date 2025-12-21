from typing import List, Optional
from app.books.models.book import Book
from app.books.repositories.book_repository import BookRepository
from app.books.schemas.author import AuthorDetail, AuthorShort
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
            cover_urls=data.cover_urls or []
        )

        cover_urls = [cover.cover_url for cover in book.covers] if book.covers else []

        return BookRead(
            id=book.id,
            title=book.title,
            subtitle=book.subtitle,
            first_publish_date=book.first_publish_date,
            description=book.description,
            cover_urls=cover_urls
        )

    @staticmethod
    async def get_short_books(
            session: AsyncSession,
            title_substring: str | None = None,
            author_substring: str | None = None,
            subject_substring: str | None = None,
            page: int = 1,
            page_size: int = 10
    ) -> PaginatedResponse:

        books, total = await BookRepository.get_books_by_filters_paginated(
            session=session,
            title_substring=title_substring,
            author_substring=author_substring,
            subject_substring=subject_substring,
            page=page,
            page_size=page_size
        )

        book_shorts = []
        for book in books:
            cover_urls = [cover.cover_url for cover in book.covers] if book.covers else []

            book_short = BookShort(
                id=book.id,
                title=book.title,
                authors=[AuthorShort.model_validate(a) for a in book.authors] if book.authors else None,
                cover_urls=cover_urls
            )
            book_shorts.append(book_short)

        return PaginatedResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=book_shorts
        )

    @staticmethod
    async def get_book_details(id: int, session: AsyncSession) -> BookDetails | None:
        book = await BookRepository.get_book_details(id, session)

        if not book:
            return None

        authors = [
            AuthorDetail(
                id=author.id,
                name=author.name,
                bio=author.bio,
                birth_date=author.birth_date,
                death_date=author.death_date,
                wikipedia=author.wikipedia
            )
            for author in book.authors
        ] if book.authors else []

        cover_urls = [cover.cover_url for cover in book.covers] if book.covers else []

        return BookDetails(
            id=book.id,
            title=book.title,
            subtitle=book.subtitle,
            first_publish_date=book.first_publish_date,
            description=book.description,
            authors=authors,
            subjects=[s.subject for s in book.subjects] if book.subjects else [],
            cover_urls=cover_urls
        )

    @staticmethod
    async def add_subject_book(data: SubjectCreate, session: AsyncSession):
        return await BookRepository.add_subject_book(data, session)