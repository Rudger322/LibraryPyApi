from typing import List, Optional

from sqlalchemy.engine.result import null_result
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.customers.models.customer import Customer


class CustomerRepository:
    @staticmethod
    async def get_all_customers(session: AsyncSession) -> List[Customer]:
        result = await session.execute(select(Customer))
        return result.scalars().all()

    @staticmethod
    async def create_customer(session: AsyncSession, customer: Customer) -> Customer:
        session.add(customer)
        await session.commit()
        await session.refresh(customer)
        return customer

    @staticmethod
    async def update_customer(session: AsyncSession, key: str, data: dict) -> Optional[Customer]:
        result = await session.execute(select(Customer).where(Customer.key == key))
        customer = result.scalar_one_or_none()

        if not customer:
            return None

        for field, value in data.items():
            if hasattr(customer, field) and field != "key":
                setattr(customer, field, value)

        session.add(customer)
        await session.commit()
        await session.refresh(customer)

        return customer