from sqlalchemy import insert
from sqlmodel import select
from app.books.models.author import Author
from app.books.schemas.author import AuthorCreate, AuthorRead
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

    @staticmethod
    async def add_author(session: AsyncSession, data: AuthorCreate):
        author = Author(
            name=data.name,
            bio=data.bio,
            birth_date=data.birth_date,
            death_date=data.death_date,
            wikipedia=data.wikipedia
        )
        session.add(author)
        await session.flush()

        book_ids = data.books_ids

        if data.books_ids:
            await session.execute(
                insert(Author.__mapper__.relationships['books'].secondary).values([
                    {"author_id": author.id, "book_id": book_id} for book_id in book_ids
                ])
            )

        await session.commit()
        await session.refresh(author)

        return AuthorRead.model_validate(author)

    #TODO: сделать для author_detail, отдельное окно в main_page
    @staticmethod
    async def get_details_author_by_id(id: int, session: AsyncSession):
        pass