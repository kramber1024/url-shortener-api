import base64
import datetime
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from app import crud

if TYPE_CHECKING:
    from typing import Literal

    from app.core.database.models import Network


def now() -> int:
    """Get current unix timestamp in seconds (UTC+0).

    Returns:
        The current unix timestamp in seconds

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
        The URL safe base 64 string.

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


async def get_country_by_ip(*, session: AsyncSession, ip: str) -> str | None:
    """Get the country code of the given ` ip `.

    Country code is a two letter code as per \
        [**ISO 3166-1 alpha-2**](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).

    Args:
        session (AsyncSession): The database session.
        ip (str): The IP address to check.

    Returns:
        Country code if found, otherwise ` None `.
    """
    octets: tuple[Literal[3], Literal[2], Literal[1]] = (3, 2, 1)
    checked_networks: set[str] = set()

    for octet in octets:
        networks: list[Network] = await crud.get_networks_by_ip(
            session=session,
            ip=ip,
            octets=octet,
        )

        for network in networks:
            if network.address in checked_networks:
                continue

            if ip in network:
                return network.country

            checked_networks.add(str(network))

    return None
