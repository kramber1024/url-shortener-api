from enum import Enum


class Phone(int, Enum):
    MIN_LENGTH: int = 7
    MAX_LENGTH: int = 16
