from datetime import date
from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base


class Issue(Base):
    __tablename__ = "issues"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    librarian_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    date_of_issue: Mapped[date] = mapped_column()
    return_until: Mapped[date] = mapped_column()
    return_date: Mapped[Optional[date]] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="issued")  # issued, returned, overdue
    notes: Mapped[Optional[str]] = mapped_column(String(500))

    # Связи
    book: Mapped["Book"] = relationship("Book", back_populates="issues")
    customer: Mapped["Customer"] = relationship("Customer", back_populates="issues")
    librarian: Mapped["User"] = relationship("User")