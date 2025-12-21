from typing import Optional, List
from sqlalchemy import select, func
from app.reports.models.customer import Customer
from app.database.db import AsyncSession


class CustomerRepository:

    @staticmethod
    async def create_customer(session: AsyncSession, customer: Customer) -> Customer:
        session.add(customer)
        await session.commit()
        await session.refresh(customer)
        return customer

    @staticmethod
    async def get_all_customers(session: AsyncSession) -> List[Customer]:
        result = await session.execute(select(Customer))
        return result.scalars().all()

    @staticmethod
    async def get_customer_by_id(session: AsyncSession, customer_id: int) -> Optional[Customer]:
        result = await session.execute(select(Customer).where(Customer.id == customer_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_customer_by_email(session: AsyncSession, email: str) -> Optional[Customer]:
        result = await session.execute(select(Customer).where(Customer.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def search_customers_by_name(session: AsyncSession, name: str) -> List[Customer]:
        result = await session.execute(
            select(Customer).where(Customer.name.ilike(f"%{name}%"))
        )
        return result.scalars().all()

    @staticmethod
    async def update_customer(session: AsyncSession, customer: Customer) -> Customer:
        await session.commit()
        await session.refresh(customer)
        return customer

    @staticmethod
    async def delete_customer(session: AsyncSession, customer: Customer) -> None:
        await session.delete(customer)
        await session.commit()


    @staticmethod
    async def get_customers_paginated(
            session: AsyncSession,
            customer_id: Optional[int] = None,
            name: Optional[str] = None,
            email: Optional[str] = None,
            page: int = 1,
            page_size: int = 10
    ) -> tuple[List[Customer], int]:

        base_query = select(Customer)
        count_query = select(func.count(Customer.id))

        # Если указан ID - возвращаем только одного
        if customer_id is not None:
            base_query = base_query.where(Customer.id == customer_id)
            count_query = count_query.where(Customer.id == customer_id)
        else:
            # Фильтры
            if name:
                base_query = base_query.where(Customer.name.ilike(f"%{name}%"))
                count_query = count_query.where(Customer.name.ilike(f"%{name}%"))

            if email:
                base_query = base_query.where(Customer.email.ilike(f"%{email}%"))
                count_query = count_query.where(Customer.email.ilike(f"%{email}%"))

        # Подсчёт общего количества
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Пагинация
        offset = (page - 1) * page_size
        base_query = base_query.limit(page_size).offset(offset)

        # Получение данных
        result = await session.execute(base_query)
        customers = result.scalars().all()

        return customers, total