import datetime


def get_current_time() -> int:
    """Get current unix timestamp in seconds (UTC+0).

    Returns
    -------
        int: The current unix timestamp in seconds

    Examples
    --------
    >>> get_current_unix_timestamp()
    1723566362

    """
    return int(datetime.datetime.now(datetime.UTC).timestamp())
