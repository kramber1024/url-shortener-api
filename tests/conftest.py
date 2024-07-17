from asyncio import current_task
from collections.abc import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session

from app.core.config import settings
from app.core.database import Database
from app.core.database import db as database
from app.core.database.models import Status, User
from app.main import app
from tests import utils


@pytest_asyncio.fixture(scope="session", autouse=True)
def setup() -> None:
    settings.db.SALT_ROUNDS = 4
    settings.db.URL = settings.db.URL.replace(
        "database.sqlite3",
        "test_database.sqlite3",
    )


@pytest_asyncio.fixture(scope="session")
async def db() -> AsyncGenerator[Database, None]:
    test_db: Database = Database(
        url=settings.db.URL,
    )
    await test_db.create_db(hard_rest=True)
    yield test_db
    await test_db.engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(db: Database) -> AsyncGenerator[AsyncSession, None]:
    async_session: async_scoped_session[AsyncSession] = async_scoped_session(
        session_factory=db.session_factory,
        scopefunc=current_task,
    )

    try:
        async with async_session() as session:
            yield session
            await session.execute(delete(User))
            await session.execute(delete(Status))
            await session.commit()

    finally:
        await async_session.remove()


@pytest_asyncio.fixture(scope="function")
async def client(db: Database) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[database.scoped_session] = db.scoped_session

    async with AsyncClient(
        transport=ASGITransport(app),  # type: ignore[arg-type]
        base_url=f"http://{settings.dev.HOST}:{settings.dev.TEST_PORT}",
        headers={"Content-Type": "application/json"},
        timeout=10,
    ) as c:
        yield c

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope="function")
async def db_user(session: AsyncSession) -> AsyncGenerator[User, None]:
    user: User = User(
        first_name="Lavon",
        last_name="Fisher",
        email="Dorris92@hotmail.com",
        password=utils.DB_USER_PASSWORD,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    status: Status = Status(
        user_id=user.id,
        active=True,
        premium=False,
    )
    session.add(status)
    await session.commit()
    await session.refresh(user)

    yield user

    await session.delete(status)
    await session.delete(user)
    await session.commit()
