from .data import Data


class FirstName(Data):
    """` User ` first name length constraints."""

    MIN_LENGTH: int = 3
    MAX_LENGTH: int = 16
