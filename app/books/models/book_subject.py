from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.db import Base

class BookSubject(Base):
    __tablename__ = "book_subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str] = mapped_column()
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    book: Mapped[Optional["Book"]] = relationship("Book", back_populates="subjects")