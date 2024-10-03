from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Network


async def create_network(
    *,
    session: AsyncSession,
    network: str,
    mask: int,
    country: str,
) -> Network:
    network_: Network = Network(
        network=network,
        mask=mask,
        country=country,
    )

    session.add(network_)
    await session.commit()
    await session.refresh(network_)
    return network_


async def get_all_networks(*, session: AsyncSession) -> list[Network]:
    result: Result[tuple[Network]] = await session.execute(
        select(Network),
    )

    networks: list[Network] = list(result.scalars().all())

    return networks
