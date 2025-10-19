from typing import List
from sqlmodel import select
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
