from datetime import date
from typing import Optional, List
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str]
    birth_date: Optional[date]
    death_date: Optional[date]
    wikipedia: Optional[str]

class AuthorCreate(AuthorBase):
    pass

class AuthorRead(AuthorBase):
    id: int
    class Config:
        from_attributes = True

class AuthorShort(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}