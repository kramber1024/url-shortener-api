from sqlalchemy import Integer
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.id_generator import id_generator


class IDMixin:
    """Mixin for models that require an ` id ` primary column.

    It generates a unique identifier using
    [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID).
    """

    _id: Mapped[int] = mapped_column(
        "id",
        Integer(),
        default=id_generator,
        nullable=False,
        primary_key=True,
        unique=True,
        sort_order=-1,
    )

    @hybrid_property
    def id(self) -> int:
        """Unique identifier for the record.

        Returns:
            int: The unique identifier for the record.
        """
        return self._id
