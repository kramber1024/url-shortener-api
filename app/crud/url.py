from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Url

if TYPE_CHECKING:
    from sqlalchemy import Result


async def create_url(
    *,
    session: AsyncSession,
    user_id: int,
    address: str,
    location: str,
) -> Url:
    url: Url = Url(
        user_id=user_id,
        address=address,
        location=location,
    )

    session.add(url)
    await session.commit()
    await session.refresh(url)
    return url


async def get_url_by_address(
    *,
    session: AsyncSession,
    address: str,
) -> Url | None:
    result: Result[tuple[Url]] = await session.execute(
        select(Url).filter(Url.address == address),
    )
    url: Url | None = result.scalars().first()

    return url
