from enum import Enum, unique


@unique
class Page(Enum):
    """Application pages."""

    NOT_FOUND = "404"
