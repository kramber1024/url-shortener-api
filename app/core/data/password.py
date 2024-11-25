from enum import Enum


class Password(int, Enum):
    MIN_LENGTH: int = 8
    MAX_LENGTH: int = 256
    HASHED_LENGTH: int = 128
