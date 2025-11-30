from datetime import date
from typing import Optional
from pydantic import BaseModel, field_validator


class IssueBase(BaseModel):
    book_id: int
    customer_id: int
    date_of_issue: date
    return_until: date
    notes: Optional[str] = None


class IssueCreate(IssueBase):
    pass


class IssueUpdate(BaseModel):
    return_until: Optional[date] = None
    notes: Optional[str] = None


class IssueReturn(BaseModel):
    return_date: date
    notes: Optional[str] = None


class IssueRead(IssueBase):
    id: int
    librarian_id: int
    return_date: Optional[date] = None
    status: str

    model_config = {"from_attributes": True}


class IssueWithDetails(BaseModel):
    id: int
    book_title: str
    customer_name: str
    librarian_name: str
    date_of_issue: date
    return_until: date
    return_date: Optional[date] = None
    status: str
    notes: Optional[str] = None

    model_config = {"from_attributes": True}