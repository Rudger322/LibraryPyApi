from sqlmodel import select
from app.books.models.author import Author
from app.database.db import AsyncSession

class AuthorRepository:

    @staticmethod
    async def get_or_create(session: AsyncSession, key: str, name: str = "Unknown") -> Author:
        result = await session.execute(select(Author).where(Author.key == key))
        author = result.scalar_one_or_none()
        if not author:
            author = Author(key=key, name=name)
            session.add(author)
            await session.commit()
            await session.refresh(author)
        return author
