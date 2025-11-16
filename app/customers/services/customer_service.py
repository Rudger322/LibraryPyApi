from sqlalchemy.ext.asyncio import AsyncSession

from app.customers.models.customer import Customer
from app.customers.repositories.customer_repository import CustomerRepository
from app.customers.schemas.customer import CustomerCreate, CustomerRead, CustomerShort, CustomerEdit


class CustomerService:

    @staticmethod
    async def add_customer(session: AsyncSession, data: CustomerCreate) -> CustomerRead:
        return await CustomerRepository.add_customer(session, data)

    @staticmethod
    async def get_customers(id: str, name, session):
        if id is not None:
            id_customers = await CustomerRepository.get_customers_by_id(id, session)
        else:
            id_customers = await CustomerRepository.get_customers(session)

        if name is not None:
            name_customers = await CustomerRepository.get_customers_by_name(name, session)
        else:
            name_customers = await CustomerRepository.get_customers(session)

        id_set = {customer.id for customer in id_customers}
        name_set = {customer.id for customer in name_customers}

        final_ids = id_set & name_set

        final_customers_obj = [customer for customer in id_customers if customer.id in final_ids]

        final_customers = [CustomerShort.model_validate(customer) for customer in final_customers_obj]

        return final_customers

    @staticmethod
    async def edit_customer(data: CustomerEdit, session: AsyncSession):
        return await CustomerRepository.edit_customer(data, session)