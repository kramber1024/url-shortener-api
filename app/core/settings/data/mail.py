from .data import Data


class Email(Data):
    """` User ` email length constraints."""

    MIN_LENGTH: int = len("a@b.c")
    MAX_LENGTH: int = 64
