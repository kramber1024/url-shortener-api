from enum import Enum


class Password(int, Enum):
    """` User ` password length constraints."""

    MIN_LENGTH = 8
    MAX_LENGTH = 256
    HASHED_LENGTH = 128
