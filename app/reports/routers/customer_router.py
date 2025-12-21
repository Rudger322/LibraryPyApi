from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from app.reports.schemas.customer import (
    CustomerCreate, CustomerRead, CustomerUpdate,
    PaginatedCustomersResponse
)
from app.reports.services.customer_service import CustomerService
from app.auth.utils.dependencies import get_current_admin_user
from app.auth.models.user import User
from app.database.db import AsyncSession, get_session

router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("/", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
async def create_customer(
        data: CustomerCreate,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_admin_user)
):
    """Создать нового читателя (только для библиотекарей)"""
    return await CustomerService.create_customer(session, data)


@router.get("/", response_model=PaginatedCustomersResponse)
async def get_customers(
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_admin_user),
        customer_id: Optional[int] = Query(None, description="ID конкретного читателя"),
        name: Optional[str] = Query(None, description="Поиск по имени (частичное совпадение)"),
        email: Optional[str] = Query(None, description="Поиск по email (частичное совпадение)"),
        page: int = Query(1, ge=1, description="Номер страницы"),
        page_size: int = Query(10, ge=1, le=100, description="Количество элементов на странице")
):

    return await CustomerService.get_customers(
        session=session,
        customer_id=customer_id,
        name=name,
        email=email,
        page=page,
        page_size=page_size
    )


@router.put("/{customer_id}", response_model=CustomerRead)
async def update_customer(
        customer_id: int,
        data: CustomerUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_admin_user)
):
    """Обновить данные читателя (только для библиотекарей)"""
    return await CustomerService.update_customer(session, customer_id, data)


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
        customer_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_admin_user)
):
    """Удалить читателя (только для библиотекарей)"""
    await CustomerService.delete_customer(session, customer_id)