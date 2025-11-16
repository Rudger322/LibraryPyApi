from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.database.db import Base
from typing import Optional

class BookCover(Base):
    __tablename__ = "book_covers"
    id: Mapped[int] = mapped_column(primary_key=True)
    cover_file: Mapped[Optional[int]] = mapped_column()
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    book: Mapped["Book"] = relationship("Book", back_populates="covers")