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
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

class BookRepository:

    @staticmethod
    async def add_book(session: AsyncSession, book: Book,
                       authors_ids: List[int],
                       subjects: List[str],
                       cover_urls: List[str]) -> Book:
        session.add(book)
        await session.flush()

        if authors_ids:
            await session.execute(
                insert(Book.__mapper__.relationships['authors'].secondary).values([
                    {"book_id": book.id, "author_id": author_id} for author_id in authors_ids
                ])
            )

        if subjects:
            for subject in subjects:
                await BookRepository.add_subject_book(SubjectCreate(
                    subject=subject,
                    book_id=book.id), session)

        if cover_urls:
            for url in cover_urls:
                cover = BookCover(
                    book_id=book.id,
                    cover_url=url
                )
                session.add(cover)

        await session.commit()
        await session.refresh(book)
        return book

    @staticmethod
    async def get_short_books_paginated(
            session: AsyncSession,
            page: int = 1,
            page_size: int = 10
    ) -> tuple[List[Book], int]:
        """
        Получить книги с пагинацией
        Возвращает: (список книг, общее количество)
        """
        # Подсчёт общего количества книг
        count_query = select(func.count(Book.id))
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Получение книг с пагинацией
        offset = (page - 1) * page_size

        query = (
            select(Book)
            .options(selectinload(Book.authors))
            .limit(page_size)
            .offset(offset)
        )

        result = await session.execute(query)
        books = result.scalars().all()

        return books, total

    @staticmethod
    async def get_books_by_title_paginated(
            title_substring: str,
            session: AsyncSession,
            page: int = 1,
            page_size: int = 10
    ) -> tuple[List[Book], int]:
        """Поиск книг по названию с пагинацией"""
        # Подсчёт общего количества
        count_query = (
            select(func.count(Book.id))
            .where(Book.title.ilike(f"%{title_substring}%"))
        )
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Получение книг с пагинацией
        offset = (page - 1) * page_size

        query = (
            select(Book)
            .options(selectinload(Book.authors))
            .where(Book.title.ilike(f"%{title_substring}%"))
            .limit(page_size)
            .offset(offset)
        )

        result = await session.execute(query)
        books = result.scalars().all()

        return books, total

    @staticmethod
    async def get_books_by_author_paginated(
            author_substring: str,
            session: AsyncSession,
            page: int = 1,
            page_size: int = 10
    ) -> tuple[List[Book], int]:
        """Поиск книг по автору с пагинацией"""
        from app.books.models.author import Author

        # Подсчёт общего количества
        count_query = (
            select(func.count(Book.id.distinct()))
            .join(Book.authors)
            .where(Author.name.ilike(f"%{author_substring}%"))
        )
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Получение книг с пагинацией
        offset = (page - 1) * page_size

        query = (
            select(Book)
            .options(selectinload(Book.authors))
            .join(Book.authors)
            .where(Author.name.ilike(f"%{author_substring}%"))
            .limit(page_size)
            .offset(offset)
        )

        result = await session.execute(query)
        books = result.scalars().unique().all()

        return books, total

    @staticmethod
    async def get_books_by_subject_paginated(
            subject_substring: str,
            session: AsyncSession,
            page: int = 1,
            page_size: int = 10
    ) -> tuple[List[Book], int]:
        """Поиск книг по теме с пагинацией"""
        from app.books.models.book_subject import BookSubject

        # Подсчёт общего количества
        count_query = (
            select(func.count(Book.id.distinct()))
            .join(Book.subjects)
            .where(BookSubject.subject.ilike(f"%{subject_substring}%"))
        )
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Получение книг с пагинацией
        offset = (page - 1) * page_size

        query = (
            select(Book)
            .options(selectinload(Book.authors))
            .join(Book.subjects)
            .where(BookSubject.subject.ilike(f"%{subject_substring}%"))
            .limit(page_size)
            .offset(offset)
        )

        result = await session.execute(query)
        books = result.scalars().unique().all()

        return books, total

    @staticmethod
    async def get_books_by_filters_paginated(
            session: AsyncSession,
            title_substring: str | None = None,
            author_substring: str | None = None,
            subject_substring: str | None = None,
            page: int = 1,
            page_size: int = 10
    ) -> tuple[List[Book], int]:
        """
        Поиск книг с несколькими фильтрами и пагинацией
        Фильтры работают по логике AND (все условия должны выполняться)
        """
        from app.books.models.author import Author
        from app.books.models.book_subject import BookSubject

        # Базовый запрос
        base_query = select(Book).options(selectinload(Book.authors))
        count_query = select(func.count(Book.id.distinct()))

        # Применяем фильтры
        if title_substring:
            base_query = base_query.where(Book.title.ilike(f"%{title_substring}%"))
            count_query = count_query.where(Book.title.ilike(f"%{title_substring}%"))

        if author_substring:
            base_query = base_query.join(Book.authors).where(
                Author.name.ilike(f"%{author_substring}%")
            )
            count_query = count_query.join(Book.authors).where(
                Author.name.ilike(f"%{author_substring}%")
            )

        if subject_substring:
            base_query = base_query.join(Book.subjects).where(
                BookSubject.subject.ilike(f"%{subject_substring}%")
            )
            count_query = count_query.join(Book.subjects).where(
                BookSubject.subject.ilike(f"%{subject_substring}%")
            )

        # Подсчёт общего количества
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Получение книг с пагинацией
        offset = (page - 1) * page_size
        base_query = base_query.limit(page_size).offset(offset)

        result = await session.execute(base_query)
        books = result.scalars().unique().all()

        return books, total

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
    async def get_book_details(id: int, session: AsyncSession) -> Book | None:
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
        return result.scalar_one_or_none()

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