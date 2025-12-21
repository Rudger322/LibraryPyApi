from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional, Literal
from app.reports.schemas.issue import (
    IssueCreate, IssueUpdate, IssueReturn,
    IssueRead, IssueWithDetails
)
from app.reports.services.issue_service import IssueService
from app.auth.utils.dependencies import get_current_admin_user
from app.auth.models.user import User
from app.database.db import AsyncSession, get_session

router = APIRouter(prefix="/issues", tags=["issues"])

@router.post("/", response_model=IssueRead, status_code=status.HTTP_201_CREATED)
async def create_issue(
    data: IssueCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Выдать книгу читателю (только для библиотекарей)"""
    return await IssueService.create_issue(session, data, current_user.id)

@router.get("/", response_model=List[IssueWithDetails])
async def get_all_issues(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Получить все выдачи (только для библиотекарей)"""
    return await IssueService.get_all_issues(session)

@router.get("/active", response_model=List[IssueWithDetails])
async def get_active_issues(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Получить активные выдачи - книги не возвращены (только для библиотекарей)"""
    return await IssueService.get_active_issues(session)


@router.get("/customer/{customer_id}", response_model=List[IssueWithDetails])
async def get_customer_issues(
        customer_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_admin_user),
        status: Optional[Literal["current", "history"]] = Query(
            None,
            description="Фильтр по статусу: 'current' - невозвращённые, 'history' - возвращённые"
        )
):
    """
    Получить выдачи конкретного читателя (только для библиотекарей)

    Примеры использования:
    - GET /issues/customer/1 - все выдачи читателя
    - GET /issues/customer/1?status=current - только текущие (не возвращённые)
    - GET /issues/customer/1?status=history - только история (возвращённые)
    """
    return await IssueService.get_customer_issues(session, customer_id, status)

@router.get("/{issue_id}", response_model=IssueWithDetails)
async def get_issue(
    issue_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Получить выдачу по ID (только для библиотекарей)"""
    return await IssueService.get_issue_by_id(session, issue_id)

@router.put("/{issue_id}/return", response_model=IssueRead)
async def return_book(
    issue_id: int,
    data: IssueReturn,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Вернуть книгу (только для библиотекарей)"""
    return await IssueService.return_book(session, issue_id, data)

@router.patch("/{issue_id}", response_model=IssueRead)
async def update_issue(
    issue_id: int,
    data: IssueUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Обновить выдачу (только для библиотекарей)"""
    return await IssueService.update_issue(session, issue_id, data)

@router.delete("/{issue_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_issue(
    issue_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Удалить выдачу (только для библиотекарей)"""
    await IssueService.delete_issue(session, issue_id)