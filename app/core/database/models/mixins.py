from datetime import datetime

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.generator import id_generator


class IDMixin:
    """Mixin for models that require an ` id ` primary column.

    Generates a unique identifier using
    [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID).

    Attributes:
        id (int): The unique identifier (Generated automatically).

    Example:
        >>> class User(Base, IDMixin): ...

    """

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        nullable=False,
        unique=True,
        sort_order=-1,
        default=id_generator,
    )


class UpdatedAtMixin:
    """Mixin for models that require an ` updated_at ` timestamp column.

    Automatically tracks the last modification time of the record.

    Attributes:
        updated_at (datetime): The timestamp indicating when
                               the record was last updated.

    Example:
        >>> class User(
        ...     Base, UpdatedAtMixin
        ... ): ...
    """

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        sort_order=0,
    )


class CreatedAtMixin:
    """Mixin for models that require a ` created_at ` timestamp column.

    Automatically sets the creation time of a record to the current timestamp
    when the record is created.

    Attributes:
        created_at (datetime): The timestamp indicating when the record was
                               created. It is automatically set to the
                               current time when the record is first created.

    Example:
        >>> class User(
        ...     Base, CreatedAtMixin
        ... ): ...
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(),
        nullable=False,
        default=func.now(),
        sort_order=1,
    )
