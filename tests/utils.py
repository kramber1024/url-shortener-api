import datetime
from typing import Any

SNOWFLAKE_RANGE: range = range(10**18, 10**19)
USER_ID: int = 1234567890123456789
USER_FIRST_NAME: str = "John"
USER_LAST_NAME: str = "Doe"
USER_EMAIL: str = "Freddie.Bosco@exAmple.com"
USER_PHONE: str = "1(234)-567-89-01"
USER_PASSWORD: str = "QKY80gAKwxebKGbWG2LPOqnSiFLanjomx8cWUzQjWuhLkueiUlhtkScUVZGdJ"


def error_type_exists(json: dict[str, Any], error_type: str) -> bool:
    errors: list[dict[str, Any]] = json.get("errors", [])
    return any(error.get("type") == error_type for error in errors)


def format_email(email: str) -> str:
    if "@" not in email:
        return email
    email_splitted: list[str] = email.split("@")

    return f"{email_splitted[0]}@{email_splitted[1].lower()}"


def get_current_time() -> int:
    """Get current unix timestamp in seconds.

    Returns
    -------
        int: The current unix timestamp in seconds

    Examples
    --------
    >>> get_current_time()
    1723566362

    """
    return int(datetime.datetime.now(datetime.UTC).timestamp())
