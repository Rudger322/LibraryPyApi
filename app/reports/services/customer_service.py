from typing import List, Optional
from fastapi import HTTPException, status
from app.reports.models.customer import Customer
from app.reports.schemas.customer import CustomerCreate, CustomerUpdate, CustomerRead
from app.reports.repositories.customer_repository import CustomerRepository
from app.database.db import AsyncSession


class CustomerService:

    @staticmethod
    async def create_customer(session: AsyncSession, data: CustomerCreate) -> CustomerRead:
        # Проверяем, существует ли email
        existing_customer = await CustomerRepository.get_customer_by_email(session, data.email)
        if existing_customer:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Customer with this email already exists"
            )

        # Создаём читателя
        customer = Customer(
            name=data.name,
            address=data.address,
            city=data.city,
            zip_code=data.zip_code,
            email=data.email,
            phone=data.phone
        )

        customer = await CustomerRepository.create_customer(session, customer)
        return CustomerRead.model_validate(customer)

    @staticmethod
    async def get_all_customers(session: AsyncSession) -> List[CustomerRead]:
        customers = await CustomerRepository.get_all_customers(session)
        return [CustomerRead.model_validate(c) for c in customers]

    @staticmethod
    async def get_customer_by_id(session: AsyncSession, customer_id: int) -> CustomerRead:
        customer = await CustomerRepository.get_customer_by_id(session, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )
        return CustomerRead.model_validate(customer)

    @staticmethod
    async def search_customers(session: AsyncSession, name: str) -> List[CustomerRead]:
        customers = await CustomerRepository.search_customers_by_name(session, name)
        return [CustomerRead.model_validate(c) for c in customers]

    @staticmethod
    async def update_customer(session: AsyncSession, customer_id: int, data: CustomerUpdate) -> CustomerRead:
        customer = await CustomerRepository.get_customer_by_id(session, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        # Обновляем только переданные поля
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)

        customer = await CustomerRepository.update_customer(session, customer)
        return CustomerRead.model_validate(customer)

    @staticmethod
    async def delete_customer(session: AsyncSession, customer_id: int) -> None:
        customer = await CustomerRepository.get_customer_by_id(session, customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found"
            )

        await CustomerRepository.delete_customer(session, customer)