from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.database.db import Base


class Showcase(Base):
    __tablename__ = "showcase"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), unique=True)
    position: Mapped[int] = mapped_column()

    book: Mapped["Book"] = relationship("Book")