from enum import Enum


class FirstName(int, Enum):
    """` User ` first name length constraints."""

    MIN_LENGTH = 3
    MAX_LENGTH = 16
