from typing import List
from app.books.models.book import Book
from app.books.repositories.book_repository import BookRepository
from app.books.schemas.book import BookCreate, BookRead, BookShort, BookDetails
from app.books.schemas.cover import CoverCreate
from app.books.schemas.subject import SubjectCreate
from app.database.db import AsyncSession

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
    async def get_book_details(id: int, session: AsyncSession) -> BookDetails | None:
        return await BookRepository.get_book_details(id, session)

    @staticmethod
    async def add_cover_book(data: CoverCreate, session: AsyncSession):
        return await BookRepository.add_cover_book(data, session)

    @staticmethod
    async def add_subject_book(data: SubjectCreate, session: AsyncSession):
        return await BookRepository.add_subject_book(data, session)