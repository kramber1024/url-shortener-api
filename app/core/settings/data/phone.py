from enum import Enum


class Phone(int, Enum):
    """` User ` phone number length constraints."""

    MIN_LENGTH = 7
    MAX_LENGTH = 16
