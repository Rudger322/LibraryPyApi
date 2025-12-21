from typing import List
from fastapi import HTTPException, status

from app.books.schemas.author import AuthorShort
from app.books.schemas.showcase import ShowcaseUpdate, ShowcaseResponse
from app.books.schemas.book import BookShort
from app.books.repositories.showcase_repository import ShowcaseRepository
from app.books.repositories.book_repository import BookRepository
from app.database.db import AsyncSession


class ShowcaseService:

    @staticmethod
    async def get_showcase(session: AsyncSession) -> ShowcaseResponse:
        """Получить книги из витрины"""
        books = await ShowcaseRepository.get_showcase_books(session)

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

        return ShowcaseResponse(
            total=len(book_shorts),
            books=book_shorts
        )

    @staticmethod
    async def set_showcase(session: AsyncSession, data: ShowcaseUpdate) -> ShowcaseResponse:
        """
        Установить книги в витрину
        Заменяет все книги в витрине на новые
        """
        # Проверяем, что все книги существуют
        for book_id in data.book_ids:
            book = await BookRepository.get_book_details(book_id, session)
            if not book:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Book with id {book_id} not found"
                )

        # Удаляем дубликаты (если фронтенд отправил одну книгу дважды)
        unique_book_ids = []
        seen = set()
        for book_id in data.book_ids:
            if book_id not in seen:
                unique_book_ids.append(book_id)
                seen.add(book_id)

        # Устанавливаем книги в витрину
        await ShowcaseRepository.set_showcase_books(session, unique_book_ids)

        # Получаем обновлённую витрину
        return await ShowcaseService.get_showcase(session)