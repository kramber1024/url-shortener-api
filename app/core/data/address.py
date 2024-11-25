from enum import Enum


class Address(int, Enum):
    MIN_LENGTH: int = len("http://a.b")
    MAX_LENGTH: int = 2048
