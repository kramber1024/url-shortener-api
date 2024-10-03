from sqlalchemy import Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.database.generator import id_generator


class Base(DeclarativeBase):
    """Concrete base class for models.

    Example:
    >>> from mixins import Base
    >>> class User(Base): ...

    """

    __abstract__: bool = True


class IDMixin:
    """Mixin for models that require an ` id ` primary column.

    Generates a unique identifier using [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID).

    Attributes:
        id (int): The unique identifier (Generated automatically).

    """

    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        nullable=False,
        unique=True,
        sort_order=-1,
        default=id_generator,
    )
