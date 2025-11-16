from app.books.models.author import Author
from app.books.repositories.author_repository import AuthorRepository
from app.books.schemas.author import AuthorCreate, AuthorRead
from app.database.db import AsyncSession

class AuthorService:

    @staticmethod
    async def add_author(session: AsyncSession, data: AuthorCreate) -> AuthorRead:
        return await AuthorRepository.add_author(session, data)

    @staticmethod
    async def get_authors(session: AsyncSession) -> Author:
        return await AuthorRepository.get_authors(session)

    @staticmethod
    async def get_author_details(id: int, session: AsyncSession) -> AuthorRead:
        author = await AuthorRepository.get_author_details(id, session)
        return AuthorRead.model_validate(author)