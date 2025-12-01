from typing import Optional
from datetime import date
from fastapi import HTTPException, status
from app.reports.schemas.reports import (
    ReminderItem, ReminderResponse,
    BookHistoryItem, BookHistoryResponse, BookInfo
)
from app.reports.repositories.reports_repository import ReportsRepository
from app.database.db import AsyncSession


class ReportsService:

    @staticmethod
    async def get_reminders(
            session: AsyncSession,
            sort_by: str = "return_until",
            order: str = "asc",
            customer_name: Optional[str] = None,
            book_title: Optional[str] = None
    ) -> ReminderResponse:
        """
        Получить список просроченных книг (Reminders tab)
        """
        issues = await ReportsRepository.get_overdue_issues(
            session, sort_by, order, customer_name, book_title
        )

        today = date.today()

        items = [
            ReminderItem(
                issue_id=issue.id,
                book_id=issue.book_id,
                title=issue.book.title,
                customer=issue.customer.name,
                date_of_issue=issue.date_of_issue,
                return_until=issue.return_until,
                days_overdue=(today - issue.return_until).days
            )
            for issue in issues
        ]

        return ReminderResponse(
            total=len(items),
            items=items
        )

    @staticmethod
    async def get_book_history(
            session: AsyncSession,
            book_id: int,
            sort_by: str = "date_of_issue",
            order: str = "desc"
    ) -> BookHistoryResponse:
        """
        Получить историю выдач книги (Book History tab)
        """
        result = await ReportsRepository.get_book_history(
            session, book_id, sort_by, order
        )

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        book, issues = result

        history_items = [
            BookHistoryItem(
                issue_id=issue.id,
                customer=issue.customer.name,
                date_of_issue=issue.date_of_issue,
                return_date=issue.return_date,
                return_until=issue.return_until,
                status=issue.status
            )
            for issue in issues
        ]

        return BookHistoryResponse(
            book=BookInfo(
                id=book.id,
                title=book.title,
                subtitle=book.subtitle
            ),
            total_issues=len(history_items),
            history=history_items
        )