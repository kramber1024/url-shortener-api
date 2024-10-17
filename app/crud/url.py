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
    """Get a ` Url ` by its slug.

    Args:
        session (AsyncSession): The database session.
        slug (str): The slug of the ` Url `.

    Returns:
        The ` Url ` instance if found, otherwise ` None `.
    """
    result: Result[tuple[Url]] = await session.execute(
        select(Url).filter(Url.slug == slug),
    )
    url: Url | None = result.scalars().first()

    return url


async def update_url(
    *,
    session: AsyncSession,
    url: Url,
    slug: str | None = None,
    address: str | None = None,
    total_clicks: int | None = None,
) -> Url:
    """Update the ` Url ` attributes with the given values.

    Args:
        session (AsyncSession): The database session.
        url (Url): The ` Url ` instance to update.
        slug (str | None, optional): New slug.
        address (str | None, optional): New address.
        total_clicks (int | None, optional): New total_clicks value.

    Returns:
        The updated ` Url ` instance.
    """
    url.slug = slug or url.slug
    url.address = address or url.address
    url.total_clicks = total_clicks or url.total_clicks

    session.add(url)
    await session.commit()
    await session.refresh(url)
    return url
