from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.customers.models.customer import Customer
from app.customers.services.customer_service import CustomerService
from app.database.db import get_session

router = APIRouter(prefix="/customers", tags=["customers"])

@router.get("/", response_model=List[Customer])
async def get_customers(session: AsyncSession = Depends(get_session)):
    return await CustomerService.get_all_customers(session)


@router.post("/", response_model=Customer)
async def create_customer(
    key: str,
    name: str,
    address: str,
    zip: str,
    city: str,
    phone: str,
    email: str,
    session: AsyncSession = Depends(get_session)
):
    return await CustomerService.add_customer(
        session, key, name, address, zip, city, phone, email
    )

@router.put("/{key}", response_model=Customer)
async def update_customer(
    key: str,
    data: dict,
    session: AsyncSession = Depends(get_session)
):
    updated_customer = await CustomerService.update_customer(session, key, data)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer