from enum import Enum


class Email(int, Enum):
    MIN_LENGTH: int = len("a@b.c")
    MAX_LENGTH: int = 64
