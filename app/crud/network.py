from ipaddress import IPv4Address
from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Network

if TYPE_CHECKING:
    from sqlalchemy import Result


async def get_network_by_ip(
    *,
    async_session: AsyncSession,
    ip: str,
) -> Network | None:
    """Retrieve a `Network` from the database by IP address.

    Args:
        async_session: The async database session.
        ip: The IP address to search for.

    Returns:
        The ` Network ` instance if found, otherwise ` None `.
    """
    ip_address: int = int(IPv4Address(ip))

    result: Result[tuple[Network]] = await async_session.execute(
        select(Network)
        .where(
            (Network.start_address <= ip_address)
            & (Network.end_address >= ip_address),
        )
        .limit(1),
    )
    network: Network | None = result.scalars().first()

    return network
