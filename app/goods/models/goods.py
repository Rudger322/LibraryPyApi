from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from decimal import Decimal


class GoodsBase(SQLModel):
    name: str
    description: str
    price: Decimal
    stock: int
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Goods(GoodsBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class GoodsCreate(SQLModel):
    name: str
    description: str
    price: Decimal
    stock: int
    category: str


class GoodsUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None
    category: Optional[str] = None
