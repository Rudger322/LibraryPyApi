from fastapi import APIRouter, Depends, status
from typing import List
from app.reports.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate
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

@router.get("/", response_model=List[CustomerRead])
async def get_all_customers(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Получить список всех читателей (только для библиотекарей)"""
    return await CustomerService.get_all_customers(session)

@router.get("/search", response_model=List[CustomerRead])
async def search_customers(
    name: str,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Поиск читателей по имени (только для библиотекарей)"""
    return await CustomerService.search_customers(session, name)

@router.get("/{customer_id}", response_model=CustomerRead)
async def get_customer(
    customer_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_admin_user)
):
    """Получить читателя по ID (только для библиотекарей)"""
    return await CustomerService.get_customer_by_id(session, customer_id)

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