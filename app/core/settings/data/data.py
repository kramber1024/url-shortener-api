class Data:
    """Base class for data classes.

    Raises:
        AttributeError: If MIN_LENGTH or MAX_LENGTH is not defined in the
            subclass.
    """

    MIN_LENGTH: int = 0
    MAX_LENGTH: int = 0

    def __init_subclass__(cls) -> None:
        for attr in ("MIN_LENGTH", "MAX_LENGTH"):
            if attr not in cls.__dict__:
                raise AttributeError

    @classmethod
    def validate_length(cls, value: str) -> bool:
        """Validate the length of the provided string.

        Args:
            value: The string to validate.

        Returns:
            ` True ` if the length of the string is within the range, ` False `
                otherwise.
        """
        return cls.MIN_LENGTH <= len(value) <= cls.MAX_LENGTH
