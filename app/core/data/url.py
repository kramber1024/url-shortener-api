from enum import Enum


class Url(int, Enum):
    MIN_LENGTH: int = len("http://a.b")
    MAX_LENGTH: int = 2048
    USER_MAX_AMOUNT: int = 2048
    USER_MAX_TAGS_AMOUNT: int = 32
