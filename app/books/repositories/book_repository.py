from typing import List, Optional
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from app.books.models import BookCover, Author
from app.books.models.book import Book
from app.books.models.book_subject import BookSubject
from app.books.schemas.book import BookShort, BookDetails
from app.books.schemas.cover import CoverCreate, CoverRead
from app.books.schemas.subject import SubjectCreate, SubjectRead
from app.database.db import AsyncSession

class BookRepository:

    @staticmethod
    async def add_book(session: AsyncSession, book: Book,
                       authors_ids: List[int],
                       subjects_ids: List[int],
                       covers_ids: List[int]) -> Book:
        session.add(book)
        await session.flush()

        if authors_ids:
            await session.execute(
                insert(Book.__mapper__.relationships['authors'].secondary).values([
                    {"book_id": book.id, "author_id": author_id} for author_id in authors_ids
                ])
            )

        if subjects_ids:
            await session.execute(
                insert(Book.__mapper__.relationships['subjects'].secondary).values([
                    {"book_id": book.id, "book_subject_id": subject_id} for subject_id in subjects_ids
                ])
            )

        if covers_ids:
            await session.execute(
                insert(Book.__mapper__.relationships['covers'].secondary).values([
                    {"book_id": book.id, "book_cover_id": cover_id} for cover_id in covers_ids
                ])
            )

        await session.commit()
        await session.refresh(book)
        return book

    @staticmethod
    async def get_short_books(session: AsyncSession) -> List[Book]:
        query = (
            select(Book)
            .options(selectinload(Book.authors))
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_books(session: AsyncSession) -> List[Book]:
        query = select(Book)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_books_by_title(title_substring: str, session: AsyncSession):
        query = select(Book).where(Book.title.contains(title_substring))
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_books_by_author(author_substring: str, session: AsyncSession):
        query = (
                select(Book)
                .options(selectinload(Book.authors))
                .join(Book.authors)
                .where(Author.name.ilike(f"%{author_substring}%"))
        )
        result = await session.execute(query)
        books = result.scalars().unique().all()
        return books

    @staticmethod
    async def get_books_by_subject(subject_substring: str, session: AsyncSession):
        query = (
            select(Book)
            .options(selectinload(Book.subjects))
            .join(Book.subjects)
            .where(BookSubject.subject.ilike(f"%{subject_substring}%"))
        )
        result = await session.execute(query)
        books = result.scalars().unique().all()
        return books

    @staticmethod
    async def get_book_details(id: int, session: AsyncSession) -> BookDetails:
        query = (
            select(Book)
            .options(
                selectinload(Book.authors),
                selectinload(Book.subjects),
                selectinload(Book.covers)
            )
            .where(Book.id == id)
        )
        result = await session.execute(query)
        book = result.scalar_one_or_none()

        if not book:
            return None

        return BookDetails(
            title=book.title,
            subtitle=book.subtitle,
            first_publish_date=book.first_publish_date,
            description=book.description,
            authors_ids=[a.id for a in book.authors] if book.authors else [],
            subjects_ids=[s.id for s in book.subjects] if book.subjects else [],
            covers_ids=[c.id for c in book.covers] if book.covers else []
        )

    @staticmethod
    async def add_cover_book(data: CoverCreate, session: AsyncSession):
        cover = BookCover(
            cover_file=data.cover_file,
            book_id=data.book_id
        )
        session.add(cover)
        await session.commit()
        await session.refresh(cover)
        return CoverRead(
            id=cover.id,
            cover_file=cover.cover_file,
            book_id=cover.book_id
        )

    @staticmethod
    async def add_subject_book(data: SubjectCreate, session: AsyncSession):
        subject = BookSubject(
            subject = data.subject,
            book_id = data.book_id
        )
        session.add(subject)
        await session.commit()
        await session.refresh(subject)
        return SubjectRead(
            id=subject.id,
            subject=subject.subject,
            book_id=subject.book_id
        )