from snowflake import SnowflakeGenerator

from app.core.settings import settings


class IDGenerator:
    """Generates unique identifiers using Snowflake ID.

    See [**Snowflake ID**](https://en.wikipedia.org/wiki/Snowflake_ID).
    """

    _snowflake_generator: SnowflakeGenerator

    def __init__(self, *, worker_id: int) -> None:
        self._snowflake_generator = SnowflakeGenerator(worker_id)

    def __call__(self) -> int:
        """Generate a unique identifier.

        Returns:
            int: The unique identifier.
        """
        return int(next(self._snowflake_generator))


id_generator: IDGenerator = IDGenerator(
    worker_id=settings.database.DATABASE_WORKER_ID,
)
