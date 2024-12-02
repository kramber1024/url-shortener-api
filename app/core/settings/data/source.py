from enum import Enum


class Source(int, Enum):
    MIN_LENGTH: int = len("http://a.b")
    MAX_LENGTH: int = 2048
