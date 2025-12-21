from typing import Optional, List, Literal
from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.reports.models.issue import Issue
from app.database.db import AsyncSession


class IssueRepository:

    @staticmethod
    async def create_issue(session: AsyncSession, issue: Issue) -> Issue:
        session.add(issue)
        await session.commit()
        await session.refresh(issue)
        return issue

    @staticmethod
    async def get_all_issues(session: AsyncSession) -> List[Issue]:
        query = (
            select(Issue)
            .options(
                selectinload(Issue.book),
                selectinload(Issue.customer),
                selectinload(Issue.librarian)
            )
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_issue_by_id(session: AsyncSession, issue_id: int) -> Optional[Issue]:
        query = (
            select(Issue)
            .options(
                selectinload(Issue.book),
                selectinload(Issue.customer),
                selectinload(Issue.librarian)
            )
            .where(Issue.id == issue_id)
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def get_active_issues(session: AsyncSession) -> List[Issue]:
        """Получить все активные выдачи (книги не возвращены)"""
        query = (
            select(Issue)
            .options(
                selectinload(Issue.book),
                selectinload(Issue.customer),
                selectinload(Issue.librarian)
            )
            .where(Issue.return_date.is_(None))
        )
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_issues_by_customer(
            session: AsyncSession,
            customer_id: int,
            status_filter: Optional[Literal["current", "history"]] = None
    ) -> List[Issue]:
        """
        Получить выдачи конкретного читателя

        status_filter:
        - "current" - только невозвращённые (return_date IS NULL)
        - "history" - только возвращённые (return_date IS NOT NULL)
        - None - все выдачи
        """
        query = (
            select(Issue)
            .options(
                selectinload(Issue.book),
                selectinload(Issue.customer),
                selectinload(Issue.librarian)
            )
            .where(Issue.customer_id == customer_id)
        )

        if status_filter == "current":
            query = query.where(Issue.return_date.is_(None))
        elif status_filter == "history":
            query = query.where(Issue.return_date.is_not(None))

        query = query.order_by(Issue.date_of_issue.desc())

        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def update_issue(session: AsyncSession, issue: Issue) -> Issue:
        await session.commit()
        await session.refresh(issue)
        return issue

    @staticmethod
    async def delete_issue(session: AsyncSession, issue: Issue) -> None:
        await session.delete(issue)
        await session.commit()

    @staticmethod
    async def check_overdue_issues(session: AsyncSession) -> None:
        """Обновить статус просроченных выдач"""
        today = date.today()
        query = (
            select(Issue)
            .where(Issue.return_date.is_(None))
            .where(Issue.return_until < today)
            .where(Issue.status != "overdue")
        )
        result = await session.execute(query)
        issues = result.scalars().all()

        for issue in issues:
            issue.status = "overdue"

        await session.commit()