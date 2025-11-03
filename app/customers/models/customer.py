from typing import Optional

from sqlmodel import Field, SQLModel


class Customer(SQLModel, table=True):
    key: str = Field(primary_key=True, max_length=128)
    name: str = Field(max_length=500)
    address: str = Field(max_length=500)
    zip: Optional[str] = Field(max_length=6)
    city: str = Field(max_length=128)
    phone: str = Field(max_length=11)
    email: Optional[str] = Field(max_length=100)