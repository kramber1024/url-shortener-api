from asyncio import current_task
from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import settings

from .models import Model


class Database:
    _async_engine: AsyncEngine
    _async_sessionmaker: async_sessionmaker[AsyncSession]
    _url: str

    def __init__(self, url: str) -> None:
        self._async_engine = create_async_engine(
            url=url,
            echo=False,
        )
        self._async_sessionmaker = async_sessionmaker(
            bind=self._async_engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )
        self._url = url.split("///")[1]

    async def get_async_session(
        self,
    ) -> AsyncGenerator[async_scoped_session[AsyncSession], None]:
        try:
            async_session: async_scoped_session[AsyncSession] = (
                async_scoped_session(
                    session_factory=self._async_sessionmaker,
                    scopefunc=current_task,
                )
            )
            yield async_session
        finally:
            await async_session.close()

    async def create_db(self, *, hard_rest: bool) -> None:
        if hard_rest and Path.exists(Path(self._url)):
            Path.unlink(Path(self._url))

        if not Path.exists(Path(self._url)):
            async with self._async_engine.begin() as connection:
                await connection.run_sync(Model.metadata.create_all)


database: Database = Database(
    url=settings.database.URL,
)
