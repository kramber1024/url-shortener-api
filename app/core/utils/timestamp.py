import datetime


def now() -> int:
    """Get the current UTC timestamp in seconds since Unix epoch."""
    return int(datetime.datetime.now(tz=datetime.UTC).timestamp())
