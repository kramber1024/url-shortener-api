from enum import Enum


class Country(int, Enum):
    """` Network ` country constraints."""

    MIN_LENGTH = len("AA")
    MAX_LENGTH = len("BB")
