from enum import Enum


class Name(int, Enum):
    """` Tag ` name length constraints."""

    MIN_LENGTH = len("a")
    MAX_LENGTH = 32
