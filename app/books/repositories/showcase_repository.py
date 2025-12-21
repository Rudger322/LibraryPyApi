from typing import List
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from app.books.models.showcase import Showcase
from app.books.models.book import Book
from app.database.db import AsyncSession


class ShowcaseRepository:

    @staticmethod
    async def clear_showcase(session: AsyncSession) -> None:
        """Очистить витрину (удалить все книги)"""
        await session.execute(delete(Showcase))
        await session.commit()

    @staticmethod
    async def set_showcase_books(session: AsyncSession, book_ids: List[int]) -> None:
        """
        Установить книги в витрину
        Сначала очищает витрину, потом добавляет новые книги
        """
        # Очистить витрину
        await session.execute(delete(Showcase))

        # Добавить новые книги с сохранением порядка
        for position, book_id in enumerate(book_ids, start=1):
            showcase_item = Showcase(
                book_id=book_id,
                position=position
            )
            session.add(showcase_item)

        await session.commit()

    @staticmethod
    async def get_showcase_books(session: AsyncSession) -> List[Book]:
        """
        Получить книги из витрины
        Возвращает книги в порядке position
        """
        query = (
            select(Book)
            .join(Showcase, Showcase.book_id == Book.id)
            .options(
                selectinload(Book.authors),
                selectinload(Book.covers)
            )
            .order_by(Showcase.position)
        )

        result = await session.execute(query)
        return result.scalars().all()