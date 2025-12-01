from typing import List, Optional
from datetime import date
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.reports.models.issue import Issue
from app.books.models.book import Book
from app.reports.models.customer import Customer
from app.database.db import AsyncSession


class ReportsRepository:

    @staticmethod
    async def get_overdue_issues(
            session: AsyncSession,
            sort_by: str = "return_until",
            order: str = "asc",
            customer_name: Optional[str] = None,
            book_title: Optional[str] = None
    ) -> List[Issue]:
        """
        Получить просроченные выдачи (книги не возвращены и срок истёк)
        """
        today = date.today()

        # Базовый запрос
        query = (
            select(Issue)
            .options(
                selectinload(Issue.book),
                selectinload(Issue.customer)
            )
            .where(Issue.return_date.is_(None))  # Книга не возвращена
            .where(Issue.return_until < today)  # Срок истёк
        )

        # Фильтр по имени клиента
        if customer_name:
            query = query.join(Issue.customer).where(
                Customer.name.ilike(f"%{customer_name}%")
            )

        # Фильтр по названию книги
        if book_title:
            query = query.join(Issue.book).where(
                Book.title.ilike(f"%{book_title}%")
            )

        # Сортировка
        if sort_by == "title":
            query = query.join(Issue.book)
            sort_field = Book.title
        elif sort_by == "customer":
            query = query.join(Issue.customer)
            sort_field = Customer.name
        elif sort_by == "date_of_issue":
            sort_field = Issue.date_of_issue
        elif sort_by == "return_until":
            sort_field = Issue.return_until
        else:
            sort_field = Issue.return_until

        # Порядок сортировки
        if order == "desc":
            query = query.order_by(sort_field.desc())
        else:
            query = query.order_by(sort_field.asc())

        result = await session.execute(query)
        return result.scalars().unique().all()

    @staticmethod
    async def get_book_history(
            session: AsyncSession,
            book_id: int,
            sort_by: str = "date_of_issue",
            order: str = "desc"
    ) -> Optional[tuple[Book, List[Issue]]]:
        """
        Получить историю выдач конкретной книги
        Возвращает: (Book, List[Issue]) или None если книга не найдена
        """
        # Получаем книгу
        book_query = select(Book).where(Book.id == book_id)
        book_result = await session.execute(book_query)
        book = book_result.scalar_one_or_none()

        if not book:
            return None

        # Получаем историю выдач
        query = (
            select(Issue)
            .options(selectinload(Issue.customer))
            .where(Issue.book_id == book_id)
        )

        # Сортировка
        if sort_by == "customer":
            query = query.join(Issue.customer).order_by(Customer.name)
        elif sort_by == "return_date":
            sort_field = Issue.return_date
        elif sort_by == "date_of_issue":
            sort_field = Issue.date_of_issue
        else:
            sort_field = Issue.date_of_issue

        if sort_by != "customer":
            if order == "desc":
                query = query.order_by(sort_field.desc())
            else:
                query = query.order_by(sort_field.asc())
        elif order == "desc":
            query = query.order_by(Customer.name.desc())

        result = await session.execute(query)
        issues = result.scalars().all()

        return book, issues