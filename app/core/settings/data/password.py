from .data import Data


class Password(Data):
    """` User ` password length constraints."""

    MIN_LENGTH: int = 8
    MAX_LENGTH: int = 256
    HASHED_LENGTH: int = 128
