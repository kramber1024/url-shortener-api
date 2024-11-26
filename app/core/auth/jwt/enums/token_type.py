from enum import Enum, unique


@unique
class TokenType(Enum):
    ACCESS: str = "access"
    REFRESH: str = "refresh"
