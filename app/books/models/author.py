from typing import Optional
from sqlmodel import SQLModel, Field

class Author(SQLModel, table=True):
    key: str = Field(primary_key=True, max_length=128)
    name: str = Field(max_length=100)
    bio: Optional[str] = None
    birth_date: Optional[str] = Field(default=None, max_length=20)
    death_date: Optional[str] = Field(default=None, max_length=20)
    wikipedia: Optional[str] = Field(default=None, max_length=255)
