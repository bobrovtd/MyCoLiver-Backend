from collections.abc import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import async_session_maker
from app.models.users import User


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that yields an async SQLAlchemy session
    """
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Dependency that yields an SQLAlchemy user database
    """
    yield SQLAlchemyUserDatabase(session, User)

