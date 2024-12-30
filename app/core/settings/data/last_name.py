from enum import Enum


class LastName(int, Enum):
    """` User ` last name length constraints."""

    MIN_LENGTH = 3
    MAX_LENGTH = 16
