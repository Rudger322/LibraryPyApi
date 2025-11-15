from app.books.models.author import Author
from app.books.repositories.author_repository import AuthorRepository
from app.books.schemas.author import AuthorCreate, AuthorRead
from app.database.db import AsyncSession

class AuthorService:

    @staticmethod
    async def add_author(session: AsyncSession, data: AuthorCreate) -> Author:
        author = Author(**data.model_dump())
        session.add(author)
        await session.commit()
        await session.refresh(author)
        return author

    @staticmethod
    async def get_authors(session: AsyncSession) -> Author:
        return await AuthorRepository.get_authors(session)