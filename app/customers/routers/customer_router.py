from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.customers.schemas.customer import CustomerCreate, CustomerRead, CustomerShort, CustomerEdit
from app.customers.services.customer_service import CustomerService
from app.database.db import get_session

router = APIRouter(prefix="/customers", tags=["customers"])

@router.post("/", response_model=CustomerRead)
async def add_customer(data: CustomerCreate, session: AsyncSession = Depends(get_session)):
    return await CustomerService.add_customer(session, data)

@router.get("/", response_model=List[CustomerShort])
async def get_customers(session: AsyncSession = Depends(get_session),
                       id: str | None = None,
                       name: str | None = None):
    return await CustomerService.get_customers(id, name, session)

@router.put("/", response_model=CustomerRead)
async def edit_customer(data: CustomerEdit, session: AsyncSession = Depends(get_session)):
    return await CustomerService.edit_customer(data, session)