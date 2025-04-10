from typing import AsyncGenerator
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config.conf import DB_HOST, DB_PORT, DB_NAME, DB_PASSWORD, DB_USER


DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def init_db():
    async with engine.begin() as conn:
        """Initializes the database by creating all tables specified in the SQLModel metadata."""
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Asynchronously creates a new session using the sessionmaker factory."""
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
