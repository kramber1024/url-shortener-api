import asyncio
from typing import Literal

from sqlalchemy import Result, Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import db
from app.core.database.models import Network


async def create_network(
    *,
    session: AsyncSession,
    address: str,
    mask: int,
    country: str,
) -> Network:
    network: Network = Network(
        address=address,
        mask=mask,
        country=country,
    )

    session.add(network)
    await session.commit()
    await session.refresh(network)
    return network


async def get_networks_by_ip(
    *,
    session: AsyncSession,
    ip: str,
    octets: Literal[1, 2, 3],
) -> list[Network]:
    """Retrieve all networks that match the first ` octets ` of the given ` ip `.

    Args:
        session (AsyncSession): The database session.
        ip (str): The IP address to match.
        octets (Literal[1, 2, 3]): The number of octets to match \
            starting from left to right.

    Returns:
        A list of ` Network ` instances that match the given ` ip `.
    """
    net = ".".join(ip.split(".")[0:octets])

    result: Result[tuple[Network]] = await session.execute(
        Select(Network).filter(
            Network.address.startswith(net),
        ),
    )
    networks: list[Network] = list(result.scalars().all())

    return networks


async def get_all_networks(*, session: AsyncSession) -> list[Network]:
    result: Result[tuple[Network]] = await session.execute(
        select(Network),
    )

    networks: list[Network] = list(result.scalars().all())

    return networks


async def main() -> None:
    session: AsyncSession = db.session_factory()

    networks: list[Network] = await get_networks_by_ip(
        session=session,
        ip="192.181.220.155",
        octets=1,
    )

    print(networks)

    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
