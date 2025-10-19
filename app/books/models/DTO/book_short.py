from typing import Optional, List
from sqlmodel import SQLModel, Field

class BookShortDTO(SQLModel):
    key: str
    title: str
    authors: List[str] = []