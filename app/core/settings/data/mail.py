from enum import Enum


class Email(int, Enum):
    """` User ` email length constraints."""

    MIN_LENGTH = len("a@b.c")
    MAX_LENGTH = 64
