from datetime import timedelta
from typing import Optional
from fastapi import HTTPException, status
from app.auth.models.user import User
from app.auth.schemas.user import UserCreate
from app.auth.repositories.user_repository import UserRepository
from app.auth.utils.security import verify_password, get_password_hash, create_access_token
from app.config.conf import ACCESS_TOKEN_EXPIRE_MINUTES
from app.database.db import AsyncSession


class AuthService:

    @staticmethod
    async def register_user(session: AsyncSession, user_data: UserCreate) -> User:

        existing_user = await UserRepository.get_user_by_username(session, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )


        existing_email = await UserRepository.get_user_by_email(session, user_data.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )


        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )

        return await UserRepository.create_user(session, user)

    @staticmethod
    async def authenticate_user(session: AsyncSession, username: str, password: str) -> Optional[User]:
        user = await UserRepository.get_user_by_username(session, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_token(username: str) -> str:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        return access_token