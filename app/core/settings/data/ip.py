from .data import Data


class IP(Data):
    """` Click ` IP address length constraints."""

    MIN_LENGTH: int = len("1.1.1.1")
    MAX_LENGTH: int = len("255.255.255.255")
