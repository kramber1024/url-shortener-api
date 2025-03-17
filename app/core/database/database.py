from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.settings import settings

from .models import Model


class Database:
    """Database manager.

    This class is responsible for managing the database interactions.
    """

    def __init__(self, url: str) -> None:
        self._async_engine: AsyncEngine = create_async_engine(
            url=url,
            echo=False,
        )
        self._async_sessionmaker: async_sessionmaker[AsyncSession] = (
            async_sessionmaker(
                bind=self._async_engine,
                autoflush=False,
                expire_on_commit=False,
                autocommit=False,
            )
        )

    async def get_async_session(self) -> AsyncGenerator[AsyncSession]:
        """Get an async session from the sessionmaker.

        This is a ` FastAPI ` dependency.
        """
        async_session: AsyncSession = self._async_sessionmaker()
        try:
            yield async_session
        finally:
            await async_session.close()

    async def shutdown(self) -> None:
        """Shutdown the database connections.

        This method must be called when the application is shutting down.
        """
        await self._async_engine.dispose(close=True)

    async def create_tables(self, *, hard_reset: bool = False) -> None:
        async with self._async_engine.begin() as async_connection:
            if hard_reset:
                await async_connection.run_sync(Model.metadata.drop_all)

            await async_connection.run_sync(Model.metadata.create_all)


database: Database = Database(
    url=settings.database.URL,
)
