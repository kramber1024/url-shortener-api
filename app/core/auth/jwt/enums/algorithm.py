from enum import Enum, unique


@unique
class Algorithm(Enum):
    HS256: str = "HS256"
