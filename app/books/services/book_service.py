from typing import List, Optional
from app.books.models.book import Book
from app.books.repositories.book_repository import BookRepository
from app.books.repositories.author_repository import AuthorRepository
from app.database.db import AsyncSession

class BookService:

    @staticmethod
    async def add_book(session: AsyncSession, key: str, title: str, author_key: str) -> Book:
        await AuthorRepository.get_or_create(session, author_key)
        book = Book(key=key, title=title)
        return await BookRepository.add_book(session, book)

    @staticmethod
    async def get_books(session: AsyncSession) -> List[Book]:
        return await BookRepository.get_all_books(session)

    @staticmethod
    async def get_all_books(session: AsyncSession, title: Optional[str] = None, author: Optional[str] = None, subject: Optional[str] = None):
        return await BookRepository.get_all_books(session, title, author, subject)

    @staticmethod
    async def get_detail_book(key: str, session: AsyncSession):
        return await BookRepository.get_detail_book(key, session)