from enum import Enum


class Mask(int, Enum):
    """` Network ` mask constraints."""

    MIN_VALUE = 0
    MAX_VALUE = 32
