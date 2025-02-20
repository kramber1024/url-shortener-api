from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    """Base class for all models.

    Examples:
        >>> class User(Model): ...
    """

    __abstract__ = True
