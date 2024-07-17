from typing import Any

SNOWFLAKE_RANGE: range = range(10**18, 10**19)
DB_USER_PASSWORD: str = "QKY80gAKwxebKGbWG2LPOqnSiFLanjomx8cWUzQjWuhLkueiUlhtkScUVZGdJ"


def error_type_exists(json: dict[str, Any], error_type: str) -> bool:
    errors: list[dict[str, Any]] = json.get("errors", [])
    return any(error.get("type") == error_type for error in errors)


def format_email(email: str) -> str:
    if "@" not in email:
        return email
    email_splitted: list[str] = email.split("@")

    return f"{email_splitted[0]}@{email_splitted[1].lower()}"
