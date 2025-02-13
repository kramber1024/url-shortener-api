import datetime


def now() -> int:
    """Get current unix timestamp in seconds (UTC+0).

    Returns:
        The current unix timestamp in seconds

    Examples:
        >>> print(now())
        1723566362
    """
    return int(datetime.datetime.now(datetime.UTC).timestamp())
