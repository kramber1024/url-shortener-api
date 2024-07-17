from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.database.generator import gen


class Base(DeclarativeBase):
    """Concrete abstract base class for models and bases."""

    __abstract__ = True


class IDBase(Base):
    """Abstract base class for all models that require an ` id ` column.

    Attributes
    ----------
        id (int): The unique identifier (Generated automatically).

    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        nullable=False,
        unique=True,
        sort_order=-1,
    )

    def __init__(self) -> None:
        self.id = gen.new_id()
