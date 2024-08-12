from sqlalchemy import Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.database.generator import gen


class Base(DeclarativeBase):
    """Concrete base class for models"""

    __abstract__ = True


class IDMixin(object):
    """Mixin for models that require an ` id ` primary column.

    Generates a unique identifier using [Snowflake ID](https://en.wikipedia.org/wiki/Snowflake_ID).

    Attributes
    ----------
        id (int): The unique identifier (Generated automatically).

    """

    @declared_attr
    def id(cls: "IDMixin") -> Mapped[int]:
        return mapped_column(
            Integer(),
            primary_key=True,
            nullable=False,
            unique=True,
            sort_order=-1,
            default=gen.new_id(),
        )
