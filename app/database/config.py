from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings

# Create the async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=(
        {"check_same_thread": False}
        if settings.DATABASE_URL.startswith("sqlite")
        else {}
    ),
)

# Create the async session factory
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    """
    Create database tables on startup.
    Note: This will be replaced by Alembic migrations in production.
    """
    from app.database.base import Base
    from app.models import User  # noqa

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
