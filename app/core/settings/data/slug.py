from enum import Enum


class Slug(int, Enum):
    """` Url ` slug length constraints."""

    MIN_LENGTH = len("a")
    MAX_LENGTH = 256
