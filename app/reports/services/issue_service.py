from typing import List
from datetime import date, timedelta
from fastapi import HTTPException, status
from app.reports.models.issue import Issue
from app.reports.schemas.issue import (
    IssueCreate, IssueUpdate, IssueReturn,
    IssueRead, IssueWithDetails
)
from app.reports.repositories.issue_repository import IssueRepository
from app.reports.repositories.customer_repository import CustomerRepository
from app.books.repositories.book_repository import BookRepository
from app.database.db import AsyncSession


class IssueService:

    @staticmethod
    async def create_issue(
            session: AsyncSession,
            data: IssueCreate,
            librarian_id: int
    ) -> IssueRead:
        """Выдать книгу читателю"""

        # Проверяем существование книги
        book = await BookRepository.get_book_details(data.book_id, session)
        if not book:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Book not found"
            )

        # Проверяем существование читателя
        customer = await CustomerRepository.get_customer_by_id(session, data.customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        # Проверяем, не выдана ли уже эта книга
        active_issues = await IssueRepository.get_active_issues(session)
        for active_issue in active_issues:
            if active_issue.book_id == data.book_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Book is already issued to another customer (Issue ID: {active_issue.id})"
                )

        # Создаём выдачу
        issue = Issue(
            book_id=data.book_id,
            customer_id=data.customer_id,
            librarian_id=librarian_id,
            date_of_issue=data.date_of_issue,
            return_until=data.return_until,
            notes=data.notes,
            status="issued"
        )

        issue = await IssueRepository.create_issue(session, issue)
        return IssueRead.model_validate(issue)

    @staticmethod
    async def get_all_issues(session: AsyncSession) -> List[IssueWithDetails]:
        """Получить все выдачи"""
        await IssueRepository.check_overdue_issues(session)
        issues = await IssueRepository.get_all_issues(session)

        return [
            IssueWithDetails(
                id=issue.id,
                book_title=issue.book.title,
                customer_name=issue.customer.name,
                librarian_name=issue.librarian.username,
                date_of_issue=issue.date_of_issue,
                return_until=issue.return_until,
                return_date=issue.return_date,
                status=issue.status,
                notes=issue.notes
            )
            for issue in issues
        ]

    @staticmethod
    async def get_issue_by_id(session: AsyncSession, issue_id: int) -> IssueWithDetails:
        """Получить выдачу по ID"""
        issue = await IssueRepository.get_issue_by_id(session, issue_id)
        if not issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Issue not found"
            )

        return IssueWithDetails(
            id=issue.id,
            book_title=issue.book.title,
            customer_name=issue.customer.name,
            librarian_name=issue.librarian.username,
            date_of_issue=issue.date_of_issue,
            return_until=issue.return_until,
            return_date=issue.return_date,
            status=issue.status,
            notes=issue.notes
        )

    @staticmethod
    async def return_book(
            session: AsyncSession,
            issue_id: int,
            data: IssueReturn
    ) -> IssueRead:
        """Вернуть книгу"""
        issue = await IssueRepository.get_issue_by_id(session, issue_id)
        if not issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Issue not found"
            )

        if issue.return_date is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Book already returned"
            )

        # Определяем статус возврата
        if data.return_date > issue.return_until:
            issue.status = "returned_late"
        else:
            issue.status = "returned_on_time"

        issue.return_date = data.return_date
        if data.notes:
            issue.notes = data.notes

        issue = await IssueRepository.update_issue(session, issue)
        return IssueRead.model_validate(issue)

    @staticmethod
    async def update_issue(
            session: AsyncSession,
            issue_id: int,
            data: IssueUpdate
    ) -> IssueRead:
        """Обновить выдачу"""
        issue = await IssueRepository.get_issue_by_id(session, issue_id)
        if not issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Issue not found"
            )

        # Обновляем только переданные поля
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(issue, field, value)

        issue = await IssueRepository.update_issue(session, issue)
        return IssueRead.model_validate(issue)

    @staticmethod
    async def delete_issue(session: AsyncSession, issue_id: int) -> None:
        """Удалить выдачу"""
        issue = await IssueRepository.get_issue_by_id(session, issue_id)
        if not issue:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Issue not found"
            )

        await IssueRepository.delete_issue(session, issue)

    @staticmethod
    async def get_active_issues(session: AsyncSession) -> List[IssueWithDetails]:
        """Получить активные выдачи (книги не возвращены)"""
        await IssueRepository.check_overdue_issues(session)
        issues = await IssueRepository.get_active_issues(session)

        return [
            IssueWithDetails(
                id=issue.id,
                book_title=issue.book.title,
                customer_name=issue.customer.name,
                librarian_name=issue.librarian.username,
                date_of_issue=issue.date_of_issue,
                return_until=issue.return_until,
                return_date=issue.return_date,
                status=issue.status,
                notes=issue.notes
            )
            for issue in issues
        ]

    @staticmethod
    async def get_customer_issues(
            session: AsyncSession,
            customer_id: int
    ) -> List[IssueWithDetails]:
        """Получить все выдачи читателя"""
        # Проверяем существование читателя
        customer = await CustomerRepository.get_customer_by_id(session, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        issues = await IssueRepository.get_issues_by_customer(session, customer_id)

        return [
            IssueWithDetails(
                id=issue.id,
                book_title=issue.book.title,
                customer_name=issue.customer.name,
                librarian_name=issue.librarian.username,
                date_of_issue=issue.date_of_issue,
                return_until=issue.return_until,
                return_date=issue.return_date,
                status=issue.status,
                notes=issue.notes
            )
            for issue in issues
        ]