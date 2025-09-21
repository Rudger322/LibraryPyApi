from typing import Optional
from sqlmodel import SQLModel, Field

class Book(SQLModel, table=True):
    key: str = Field(primary_key=True, max_length=128)
    title: str = Field(max_length=500)
    subtitle: Optional[str] = Field(default=None, max_length=500)
    first_publish_date: Optional[str] = Field(default=None, max_length=20)
    description: Optional[str] = None
