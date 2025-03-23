import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Database


@pytest.fixture(scope="module")
def url() -> str:
    return "sqlite+aiosqlite:///tests/core/database/test_database.sqlite3"


@pytest.fixture()
def database(url: str) -> Database:
    return Database(url=url)


@pytest.mark.asyncio()
async def test_database_init(url: str) -> None:
    database: Database = Database(url=url)

    assert str(database._async_engine.url) == url
    assert database._async_sessionmaker


@pytest.mark.asyncio()
async def test_database_get_async_session(database: Database) -> None:
    async_session: AsyncSession = await anext(database.get_async_session())

    assert isinstance(async_session, AsyncSession)
    assert async_session.is_active


@pytest.mark.asyncio()
async def test_database_shutdown(database: Database) -> None:
    await database.shutdown()


@pytest.mark.asyncio()
@pytest.mark.parametrize("hard_reset", [True, False])
async def test_database_create_tables(
    hard_reset: bool,
    database: Database,
) -> None:
    await database.create_tables(hard_reset=hard_reset)
