from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database import Database
from app.core.database.models import User
from app.core.settings import settings


@pytest.fixture(scope="session", autouse=True)
def setup() -> None:
    settings.database.SALT_ROUNDS = 4
    settings.database.URL = (
        "sqlite+aiosqlite:///tests/core/database/database.sqlite3"
    )


@pytest_asyncio.fixture()
async def database() -> AsyncGenerator[Database, None]:
    database: Database = Database(url=settings.database.URL)

    await database.create_tables(hard_reset=True)
    yield database
    await database.shutdown()


@pytest_asyncio.fixture()
async def async_session(
    database: Database,
) -> AsyncGenerator[AsyncSession, None]:
    async_session: AsyncSession = database._async_sessionmaker()
    try:
        yield async_session
    finally:
        await async_session.close()


@pytest_asyncio.fixture()
async def user(async_session: AsyncSession) -> User:
    return await crud.create_user(
        async_session=async_session,
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password="password" * 8,
    )
