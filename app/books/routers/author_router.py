from fastapi import APIRouter, Depends
from typing import List, Optional

from app.books.schemas.author import AuthorRead, AuthorCreate
from app.books.services.author_service import AuthorService

from app.database.db import get_session, AsyncSession

router = APIRouter(prefix="/authors", tags=["authors"])

@router.post("/", response_model=AuthorRead)
async def create_author(data: AuthorCreate, session: AsyncSession = Depends(get_session)):
    return await AuthorService.add_author(session, data)

@router.get("/", response_model=List[AuthorRead])
async def get_authors(session: AsyncSession = Depends(get_session)):
    return await AuthorService.get_authors(session)