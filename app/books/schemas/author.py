from datetime import date
from typing import Optional, List
from pydantic import BaseModel


class AuthorBase(BaseModel):
    name: str
    bio: Optional[str]
    birth_date: Optional[date]
    death_date: Optional[date]
    wikipedia: Optional[str]

class AuthorRead(AuthorBase):
    id: int
    class Config:
        from_attributes = True

class AuthorShort(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class AuthorDetail(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None
    birth_date: Optional[date] = None
    death_date: Optional[date] = None
    wikipedia: Optional[str] = None

    model_config = {"from_attributes": True}