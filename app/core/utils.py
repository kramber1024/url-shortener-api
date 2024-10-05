import base64
import datetime

from sqlalchemy.ext.asyncio import AsyncSession


def now() -> int:
    """Get current unix timestamp in seconds (UTC+0).

    Returns:
        int: The current unix timestamp in seconds

    Examples:
    >>> print(now())
    1723566362

    """
    return int(datetime.datetime.now(datetime.UTC).timestamp())


def base10_to_urlsafe_base64(number: int, /) -> str:
    """Convert a base 10 number to a URL safe base 64 string.

    Args:
        number (int): The base 10 number to convert.

    Returns:
        str: The URL safe base 64 string.

    Examples:
    >>> url_safe_base64 = (
    ...     base10_to_urlsafe_base64(
    ...         123456789
    ...     )
    ... )
    >>> print(url_safe_base64)
    "B1vNFQ"

    """
    byte_representation: bytes = number.to_bytes(
        (number.bit_length() + 7) // 8,
        byteorder="big",
    )

    base64_encoded: bytes = base64.b64encode(byte_representation)

    return (
        base64_encoded.decode("utf-8").replace("+", "-").replace("/", "_").rstrip("=")
    )


def get_country_by_ip(*, session: AsyncSession, ip: str) -> str | None:
    return None
