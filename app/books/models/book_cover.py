from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String
from app.database.db import Base
from typing import Optional

class BookCover(Base):
    __tablename__ = "book_covers"
    id: Mapped[int] = mapped_column(primary_key=True)
    cover_file: Mapped[str] = mapped_column(String(500))  # Путь к файлу
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    book: Mapped["Book"] = relationship("Book", back_populates="covers")