from enum import Enum


class Slug(int, Enum):
    MIN_LENGTH: int = len("a")
    MAX_LENGTH: int = 256
