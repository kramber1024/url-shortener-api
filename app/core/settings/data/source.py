from enum import Enum


class Source(int, Enum):
    """` Url ` source length constraints."""

    MIN_LENGTH = len("http://a.b")
    MAX_LENGTH = 2048
