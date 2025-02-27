from .data import Data


class Slug(Data):
    """` Url ` slug length constraints."""

    MIN_LENGTH: int = len("a")
    MAX_LENGTH: int = 256
