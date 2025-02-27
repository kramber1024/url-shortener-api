from .data import Data


class Source(Data):
    """` Url ` source length constraints."""

    MIN_LENGTH: int = len("http://a.b")
    MAX_LENGTH: int = 2048
