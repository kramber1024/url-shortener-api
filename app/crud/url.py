from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Url

if TYPE_CHECKING:
    from sqlalchemy import Result


async def create_url(
    *,
    async_session: AsyncSession,
    user_id: int,
    source: str,
    slug: str,
) -> Url:
    """Initialize a new ` Url ` and commit it to the database.

    Args:
        async_session: The async database session.
        user_id: The unique identifier of the ` User `.
        source: The original URL address.
        slug: The unique slug that identifies the shortened URL.

    Returns:
        The newly created ` Url ` instance.
    """
    url: Url = Url(
        user_id=user_id,
        source=source,
        slug=slug,
    )

    async_session.add(url)
    await async_session.commit()
    await async_session.refresh(url)

    return url


async def get_url_by_slug(
    *,
    async_session: AsyncSession,
    slug: str,
) -> Url | None:
    """Retrieve a ` Url ` from the database by its slug.

    Args:
        async_session: The async database session.
        slug: The unique slug that identifies the shortened URL.

    Returns:
        The ` Url ` instance if found, otherwise ` None `.
    """
    result: Result[tuple[Url]] = await async_session.execute(
        select(Url).where(Url.slug == slug),
    )
    url: Url | None = result.scalars().first()

    return url


async def update_url(
    *,
    async_session: AsyncSession,
    url: Url,
    source: str,
    slug: str,
    total_clicks: int,
) -> Url:
    """Update a ` Url ` and commit the changes to the database.

    Args:
        async_session: The async database session.
        url: The ` Url ` to update.
        source: The new original URL address.
        slug: The new unique slug that identifies the shortened URL.
        total_clicks: The new total number of ` Click `'s.

    Returns:
        The updated ` Url ` instance.
    """
    url.source = source
    url.slug = slug
    url.total_clicks = total_clicks

    async_session.add(url)
    await async_session.commit()
    await async_session.refresh(url)

    return url
