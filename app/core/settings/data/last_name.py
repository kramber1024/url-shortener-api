from .data import Data


class LastName(Data):
    """` User ` last name length constraints."""

    MIN_LENGTH: int = 3
    MAX_LENGTH: int = 16
