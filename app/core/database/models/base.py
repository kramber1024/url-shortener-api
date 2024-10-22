from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Concrete base class for models.

    Example:
        >>> class User(Base): ...

    """

    __abstract__: bool = True
