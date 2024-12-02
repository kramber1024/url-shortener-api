from typing import Any, Literal

from app.core.settings import settings

SNOWFLAKE_RANGE: range = range(10**18, 10**19)
USER_ID: int = 1234567890123456789
USER_FIRST_NAME: str = "John"
USER_LAST_NAME: str = "Doe"
USER_EMAIL: str = "Freddie.Bosco@exAmple.com"
USER_PHONE: str = "1(234)-567-89-01"
USER_PASSWORD: str = (
    "QKY80gAKwxebKGbWG2LPOqnSiFLanjomx8cWUzQjWuhLkueiUlhtkScUVZGdJ"
)


def error_type_exists(json: dict[str, Any], error_type: str) -> bool:
    errors: list[dict[str, Any]] = json.get("errors", [])
    return any(error.get("type") == error_type for error in errors)


def format_email(email: str, /) -> str:
    if "@" not in email:
        return email
    email_splitted: list[str] = email.split("@")

    return f"{email_splitted[0]}@{email_splitted[1].lower()}"


def get_token_exp(
    jwt_type: Literal["access", "refresh"],
    /,
    *,
    current_time: int,
) -> int:
    """Get the expiration time for a JWT token.

    Args:
        jwt_type (Literal["access", "refresh"]): The type of JWT token. Can be
                                                 either "access" or "refresh".
        current_time (int): The current time in seconds since the epoch.

    Returns:
        int: The expiration time in seconds since the epoch.
    """
    if jwt_type == "access":
        return current_time + settings.jwt.ACCESS_TOKEN_EXPIRES_MINUTES * 60

    return current_time + settings.jwt.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 60
