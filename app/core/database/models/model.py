from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    """Concrete base class for models.

    Examples:
        >>> class User(Model): ...
    """

    __abstract__ = True
