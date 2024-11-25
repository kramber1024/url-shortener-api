from enum import Enum


class Tag(int, Enum):
    MIN_LENGTH: int = len("a")
    MAX_LENGTH: int = 32
