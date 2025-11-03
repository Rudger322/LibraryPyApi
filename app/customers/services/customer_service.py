from typing import List, Optional

from sqlmodel.ext.asyncio.session import AsyncSession

from app.customers.models.customer import Customer
from app.customers.repositories.customer_repository import CustomerRepository


class CustomerService:

    @staticmethod
    async def get_all_customers(session: AsyncSession):
        return await CustomerRepository.get_all_customers(session)

    @staticmethod
    async def add_customer(session: AsyncSession,
                                key: str,
                                name: str,
                                address: str,
                                zip: str,
                                city: str,
                                phone: str,
                                email: str) -> Customer:
        customer = Customer(
            key=key,
            name=name,
            address=address,
            zip=zip,
            city=city,
            phone=phone,
            email=email
        )

        return await CustomerRepository.create_customer(session, customer)

    @staticmethod
    async def update_customer(session: AsyncSession,
                              key: str,
                              data: dict) -> Optional[Customer]:
        return await CustomerRepository.update_customer(session, key, data)