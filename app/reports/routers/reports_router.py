from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from typing import Optional
from io import StringIO
import csv

from app.reports.schemas.reports import ReminderResponse, BookHistoryResponse
from app.reports.services.reports_service import ReportsService
from app.auth.utils.dependencies import get_current_admin_user
from app.auth.models.user import User
from app.database.db import AsyncSession, get_session

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/reminders", response_model=ReminderResponse)
async def get_reminders(
        sort_by: str = Query("return_until",
                             description="Поле для сортировки: title, customer, date_of_issue, return_until"),
        order: str = Query("asc", description="Порядок: asc или desc"),
        customer_name: Optional[str] = Query(None, description="Фильтр по имени клиента"),
        book_title: Optional[str] = Query(None, description="Фильтр по названию книги"),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_admin_user)
):
    """
    Получить список просроченных книг (Reminders tab)

    Вкладка Reminders отображает все книги, по которым истек срок возврата,
    и книга не была возвращена читателем.
    """
    return await ReportsService.get_reminders(
        session, sort_by, order, customer_name, book_title
    )


@router.get("/reminders/export")
async def export_reminders(
        sort_by: str = Query("return_until", description="Поле для сортировки"),
        order: str = Query("asc", description="Порядок: asc или desc"),
        customer_name: Optional[str] = Query(None, description="Фильтр по имени клиента"),
        book_title: Optional[str] = Query(None, description="Фильтр по названию книги"),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_admin_user)
):
    """
    Экспорт списка просроченных книг в CSV

    Выгружает таблицу в файл формата .csv с текущей сортировкой и фильтрами.
    """
    data = await ReportsService.get_reminders(
        session, sort_by, order, customer_name, book_title
    )

    # Создаём CSV в памяти
    output = StringIO()
    writer = csv.writer(output)

    # Заголовки
    writer.writerow(['Title', 'Customer', 'Date of Issue', 'Return Until', 'Days Overdue'])

    # Данные
    for item in data.items:
        writer.writerow([
            item.title,
            item.customer,
            item.date_of_issue.strftime('%Y-%m-%d'),
            item.return_until.strftime('%Y-%m-%d'),
            item.days_overdue
        ])

    # Возвращаем CSV файл
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=reminders.csv"}
    )


@router.get("/book-history/{book_id}", response_model=BookHistoryResponse)
async def get_book_history(
        book_id: int,
        sort_by: str = Query("date_of_issue", description="Поле для сортировки: date_of_issue, return_date, customer"),
        order: str = Query("desc", description="Порядок: asc или desc"),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_admin_user)
):
    """
    Получить историю выдач книги (Book History tab)

    Вкладка Book History отображает историю всех выдач выбранной книги.
    Если книга не найдена - возвращается ошибка 404.
    """
    return await ReportsService.get_book_history(
        session, book_id, sort_by, order
    )


@router.get("/book-history/{book_id}/export")
async def export_book_history(
        book_id: int,
        sort_by: str = Query("date_of_issue", description="Поле для сортировки"),
        order: str = Query("desc", description="Порядок: asc или desc"),
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_admin_user)
):
    """
    Экспорт истории выдач книги в CSV

    Сохраняет таблицу истории в .csv файл с текущим порядком сортировки.
    """
    data = await ReportsService.get_book_history(
        session, book_id, sort_by, order
    )

    # Создаём CSV в памяти
    output = StringIO()
    writer = csv.writer(output)

    # Заголовки
    writer.writerow(['Customer', 'Date of Issue', 'Return Date', 'Return Until', 'Status'])

    # Данные
    for item in data.history:
        writer.writerow([
            item.customer,
            item.date_of_issue.strftime('%Y-%m-%d'),
            item.return_date.strftime('%Y-%m-%d') if item.return_date else 'Not returned',
            item.return_until.strftime('%Y-%m-%d'),
            item.status
        ])

    # Возвращаем CSV файл
    output.seek(0)
    filename = f"book_history_{data.book.title.replace(' ', '_')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )