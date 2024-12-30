from enum import Enum


class User(int, Enum):
    """` User ` related constraints."""

    MAX_URL_AMOUNT = 512
    MAX_TAGS_PER_URL = 32
