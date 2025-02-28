from .data import Data


class Phone(Data):
    """` User ` phone number length constraints."""

    MIN_LENGTH: int = 7
    MAX_LENGTH: int = 16
