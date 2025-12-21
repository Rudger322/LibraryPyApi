from fastapi import APIRouter, Depends
from app.books.schemas.showcase import ShowcaseUpdate, ShowcaseResponse
from app.books.services.showcase_service import ShowcaseService
from app.auth.utils.dependencies import get_current_admin_user
from app.auth.models.user import User
from app.database.db import AsyncSession, get_session

router = APIRouter(prefix="/showcase", tags=["showcase"])


@router.post("/", response_model=ShowcaseResponse)
async def set_showcase(
        data: ShowcaseUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_admin_user)
):
    """
    Установить книги в витрину (только для библиотекарей)

    Заменяет все книги в витрине на новые.
    Порядок книг в массиве определяет порядок отображения на главной странице.

    Пример:
    {
      "book_ids": [5, 12, 3, 8]
    }
    """
    return await ShowcaseService.set_showcase(session, data)


@router.get("/", response_model=ShowcaseResponse)
async def get_showcase(
        session: AsyncSession = Depends(get_session)
):
    """
    Получить книги из витрины

    Возвращает список избранных книг в порядке, установленном библиотекарем.
    Публичный эндпоинт - доступен без авторизации.
    """
    return await ShowcaseService.get_showcase(session)