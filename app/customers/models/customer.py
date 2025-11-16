from typing import Optional
from app.database.db import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    address: Mapped[Optional[str]] = mapped_column(String(500))
    zip: Mapped[int] = mapped_column()
    city: Mapped[str] = mapped_column()
    phone: Mapped[int] = mapped_column()
    email: Mapped[str] = mapped_column()