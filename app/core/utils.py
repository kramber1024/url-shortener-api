import datetime


def now() -> int:
    """Get current unix timestamp in seconds (UTC+0).

    Returns
    -------
        int: The current unix timestamp in seconds

    Examples
    --------
    >>> now()
    1723566362

    """
    return int(datetime.datetime.now(datetime.UTC).timestamp())
