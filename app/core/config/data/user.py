from enum import Enum, unique


@unique
class User(int, Enum):
    MAX_URL_AMOUNT: int = 512
    MAX_TAGS_PER_URL: int = 32
