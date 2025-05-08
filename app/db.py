# This file re-exports from database.config for backward compatibility
from app.database.config import engine, async_session_maker
from app.database.base import Base


async def create_db_and_tables():
    """Create all tables in the database"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Use the dependencies from app.database.deps instead of defining them here
from app.database.deps import get_async_session, get_user_db
