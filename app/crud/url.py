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
    slug: str,
    address: str,
) -> Url:
    url: Url = Url(
        user_id=user_id,
        slug=slug,
        address=address,
    )

    session.add(url)
    await session.commit()
    await session.refresh(url)
    return url


async def get_url_by_slug(
    *,
    session: AsyncSession,
    slug: str,
) -> Url | None:
    result: Result[tuple[Url]] = await session.execute(
        select(Url).filter(Url.slug == slug),
    )
    url: Url | None = result.scalars().first()

    return url
