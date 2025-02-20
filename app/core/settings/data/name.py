from .data import Data


class Name(Data):
    """` Tag ` name length constraints."""

    MIN_LENGTH: int = len("a")
    MAX_LENGTH: int = 32
