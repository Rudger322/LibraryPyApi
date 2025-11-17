from typing import Optional
from sqlalchemy import select
from app.auth.models.user import User
from app.database.db import AsyncSession


class UserRepository:

    @staticmethod
    async def create_user(session: AsyncSession, user: User) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def get_user_by_username(session: AsyncSession, username: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()