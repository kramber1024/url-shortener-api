from enum import Enum


class Address(int, Enum):
    """` Network ` address constraints."""

    MIN_LENGTH = len("8.8.8.8")
    MAX_LENGTH = len("255.255.255.255")
