from datetime import date
from typing import Optional, List
from pydantic import BaseModel


class CustomerBase(BaseModel):
    name: str
    address: str
    zip: int
    city: str
    phone: int
    email: str

class CustomerCreate(CustomerBase):
    pass

class CustomerShort(BaseModel):
    id: str
    name: str
    address: str
    zip: int
    city: str

    class Config:
        from_attributes = True

class CustomerRead(CustomerCreate):
    id: str

    class Config:
        from_attributes = True

class CustomerEdit(CustomerRead):
    pass