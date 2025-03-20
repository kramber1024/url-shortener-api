from snowflake import SnowflakeGenerator

from app.core.settings import settings


class IdGenerator:
    """Generator for unique identifiers using the Snowflake ID.

    See [**Snowflake ID**](https://en.wikipedia.org/wiki/Snowflake_ID).
    """

    def __init__(self, *, machine_id: int) -> None:
        """Initialize the IdGenerator.

        Args:
            machine_id: The machine ID to ensure uniqueness across different
                machines. This ID should be unique for each instance of the
                generator.
        """
        self._snowflake_generator: SnowflakeGenerator = SnowflakeGenerator(
            instance=machine_id,
            seq=0,
            epoch=0,
            timestamp=None,
        )

    def __call__(self) -> int:
        """Generate a unique identifier.

        Each call will produce a new unique identifier.

        Returns:
            The unique identifier.
        """
        return int(next(self._snowflake_generator))


id_generator: IdGenerator = IdGenerator(
    machine_id=settings.database.MACHINE_ID,
)
"""The single instance of the IdGenerator."""
