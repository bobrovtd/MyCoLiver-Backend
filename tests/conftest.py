import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.database.base import Base
from app.app import create_application
from app.database.deps import get_async_session
from app.models import User
from app.core.config import settings

# Set test database
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_db.db"
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

# Create test engine and session
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    poolclass=NullPool,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture
async def test_engine() -> AsyncEngine:
    """
    Create a test engine
    """
    return test_engine


@pytest_asyncio.fixture
async def create_test_database() -> AsyncGenerator[None, None]:
    """
    Create test database and tables
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(create_test_database) -> AsyncGenerator[AsyncSession, None]:
    """
    Get test database session
    """
    async with TestingSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def app(db_session) -> FastAPI:
    """
    Create a test app with mocked dependencies
    """
    app = create_application()

    async def get_test_db():
        try:
            yield db_session
        finally:
            pass

    # Override the get_async_session dependency
    app.dependency_overrides[get_async_session] = get_test_db

    return app


@pytest_asyncio.fixture
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    """
    Create a test client
    """
    async with AsyncClient(
        app=app,
        base_url=f"http://test{settings.API_V1_STR}",
        follow_redirects=True,
    ) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an instance of the default event loop for each test session
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
