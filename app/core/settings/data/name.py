from enum import Enum, unique


@unique
class Name(int, Enum):
    MIN_LENGTH: int = len("a")
    MAX_LENGTH: int = 32
