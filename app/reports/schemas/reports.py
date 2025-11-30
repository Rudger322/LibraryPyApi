from datetime import date
from typing import List, Optional
from pydantic import BaseModel


# Для вкладки Reminders (просроченные книги)
class ReminderItem(BaseModel):
    """Одна запись о просроченной книге"""
    issue_id: int
    book_id: int
    title: str
    customer: str
    date_of_issue: date
    return_until: date
    days_overdue: int

    model_config = {"from_attributes": True}


class ReminderResponse(BaseModel):
    """Ответ для вкладки Reminders"""
    total: int
    items: List[ReminderItem]


# Для вкладки Book History (история выдач книги)
class BookHistoryItem(BaseModel):
    """Одна запись из истории выдач книги"""
    issue_id: int
    customer: str
    date_of_issue: date
    return_date: Optional[date]
    return_until: date
    status: str  # returned_on_time, returned_late, overdue, issued

    model_config = {"from_attributes": True}


class BookInfo(BaseModel):
    """Информация о книге"""
    id: int
    title: str
    subtitle: Optional[str] = None

    model_config = {"from_attributes": True}


class BookHistoryResponse(BaseModel):
    """Ответ для вкладки Book History"""
    book: BookInfo
    total_issues: int
    history: List[BookHistoryItem]