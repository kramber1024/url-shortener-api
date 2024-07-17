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

from app.core.config import settings
from app.core.database.models.bases import Base


class Database:
    engine: AsyncEngine
    session_factory: async_sessionmaker[AsyncSession]
    url: str

    def __init__(self, url: str, *, debug: bool) -> None:
        self.engine = create_async_engine(
            url=url,
            echo=debug,
        )

        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autocommit=False,
            autoflush=False,
            expire_on_commit=False,
        )

        self.url = url.split("///")[1]

    async def scoped_session(
        self,
    ) -> AsyncGenerator[async_scoped_session[AsyncSession], None]:
        try:
            session: async_scoped_session[AsyncSession] = async_scoped_session(
                session_factory=self.session_factory,
                scopefunc=current_task,
            )
            yield session
        finally:
            await session.close()

    async def create_db(self, *, hard_rest: bool) -> None:
        if hard_rest and Path.exists(Path(self.url)):
            Path.unlink(Path(self.url))

        if not Path.exists(Path(self.url)):
            async with self.engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)


db: Database = Database(
    url=settings.db.URL,
    debug=settings.app.state.DEBUG,
)
