from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column


class UpdatedAtMixin:
    """Mixin for models that require an ` updated_at ` timestamp column.

    Automatically tracks the last modification time of the record.

    Attributes:
        updated_at (datetime): The timestamp indicating when
                               the record was last updated.

    Example:
        >>> class User(
        ...     Model, UpdatedAtMixin
        ... ): ...
    """

    __abstract__ = True

    _updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        DateTime(),
        nullable=False,
        default=func.now(),
        onupdate=func.now(),
        sort_order=0,
    )

    @hybrid_property
    def updated_at(self) -> datetime:
        return self._updated_at
