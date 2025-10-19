from typing import List, Optional
from sqlmodel import select

from app.books.models.DTO.book_details import BookDetailsDTO
from app.books.models.DTO.book_short import BookShortDTO
from app.books.models.book import Book
from app.database.db import AsyncSession

class BookRepository:

    @staticmethod
    async def add_book(session: AsyncSession, book: Book) -> Book:
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    @staticmethod
    async def get_all_books(session: AsyncSession) -> List[Book]:
        result = await session.execute(select(Book))
        return result.scalars().all()

    @staticmethod
    async def get_all_books(session: AsyncSession,
                            title: Optional[str] = None,
                            author: Optional[str] = None,
                            subject: Optional[str] = None) -> List[BookShortDTO]:
        result = await session.execute(select(Book))
        return result.scalars().all()

    @staticmethod
    async def get_detail_book(session: AsyncSession, key: str) -> BookDetailsDTO:
        result = await session.execute(select(BookDetailsDTO))