from datetime import date
from typing import Optional, List
from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    zip_code: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class CustomerRead(CustomerBase):
    id: int
    registration_date: date

    model_config = {"from_attributes": True}


class CustomerShort(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class PaginatedCustomersResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[CustomerRead]

    model_config = {"from_attributes": True}