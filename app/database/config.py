from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings
from app.database.base import Base
from app.models import User  # noqa

# Определяем URL базы данных, используя настройки проекта
DATABASE_URL = settings.DATABASE_URL

# Создаем асинхронный движок с правильными параметрами подключения
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.DEBUG,
    connect_args=(
        {"check_same_thread": False}
        if DATABASE_URL.startswith("sqlite")
        else {}
    ),
)

# Создаем фабрику асинхронных сессий
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    """
    Создает таблицы базы данных при запуске.
    Примечание: В production это будет заменено миграциями Alembic.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
