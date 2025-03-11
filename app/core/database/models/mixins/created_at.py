from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    """Mixin for models that require a created_at timestamp column.

    Automatically sets the creation time of a record.
    """

    _created_at: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime(),
        default=func.now(),
        nullable=False,
        sort_order=1,
    )

    @hybrid_property
    def created_at(self) -> datetime:
        """The timestamp indicating when the record was created."""
        return self._created_at
