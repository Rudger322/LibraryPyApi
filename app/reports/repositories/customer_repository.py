from typing import Optional, List
from sqlalchemy import select
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