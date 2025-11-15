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

    @staticmethod
    async def get_authors(session: AsyncSession):
        query = select(Author)
        result = await session.execute(query)
        return result.scalars().all()

    #TODO: сделать для author_detail, отдельное окно в main_page
    @staticmethod
    async def get_details_author_by_id(id: int, session: AsyncSession):
        pass