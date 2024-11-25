from enum import Enum


class FirstName(int, Enum):
    MIN_LENGTH: int = 3
    MAX_LENGTH: int = 16
