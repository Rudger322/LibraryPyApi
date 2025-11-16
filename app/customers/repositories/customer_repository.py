from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count, func

from app.customers.models.customer import Customer
from app.customers.schemas.customer import CustomerCreate, CustomerRead, CustomerEdit


class CustomerRepository:

    @staticmethod
    async def add_customer(session: AsyncSession, data: CustomerCreate):
        result_count = await session.execute(select(func.count(Customer.id)))
        id_count = result_count.scalar_one()
        customer = Customer(
            id="C" + str(id_count),
            name=data.name,
            address=data.address,
            zip=data.zip,
            city=data.city,
            phone=data.phone,
            email=data.email
        )
        session.add(customer)
        await session.commit()
        await session.refresh(customer)
        return CustomerRead.model_validate(customer)


    @staticmethod
    async def get_customers_by_id(id: str, session: AsyncSession):
        query = (
            select(Customer)
            .where(Customer.id.ilike(f"%{id}%"))
        )
        result = await session.execute(query)
        customers = result.scalars().unique().all()
        return customers


    @staticmethod
    async def get_customers_by_name(name: str, session: AsyncSession):
        query = (
            select(Customer)
            .where(Customer.name.ilike(f"%{name}%"))
        )
        result = await session.execute(query)
        customers = result.scalars().unique().all()
        return customers

    @staticmethod
    async def get_customers(session: AsyncSession):
        query = select(Customer)
        result = await session.execute(query)
        customers = result.scalars().all()
        return customers

    @staticmethod
    async def edit_customer(data: CustomerEdit, session: AsyncSession):
        query = select(Customer).where(Customer.id == data.id)
        result = await session.execute(query)
        customer = result.scalars().first()

        customer.name = data.name
        customer.address = data.address
        customer.zip = data.zip
        customer.city = data.city
        customer.phone = data.phone
        customer.email = data.email

        await session.commit()
        await session.refresh(customer)

        return customer
