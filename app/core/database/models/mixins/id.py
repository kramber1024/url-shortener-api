from sqlalchemy import BigInteger
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database.id_generator import id_generator


class IdMixin:
    """Mixin for models that require an id primary column.

    Automatically sets the id of a record to a unique identifier when the record
    is created.
    """

    _id: Mapped[int] = mapped_column(
        "id",
        BigInteger(),
        default=id_generator,
        nullable=False,
        primary_key=True,
        unique=True,
        sort_order=-1,
    )

    @hybrid_property
    def id(self) -> int:
        """The unique identifier of the record."""
        return self._id
