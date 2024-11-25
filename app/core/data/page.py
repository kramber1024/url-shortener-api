from enum import Enum, unique


@unique
class Page(Enum):
    NOT_FOUND: str = "404"
