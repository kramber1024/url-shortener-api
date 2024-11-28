from typing import TYPE_CHECKING

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Url

if TYPE_CHECKING:
    from sqlalchemy import Result


async def create_url(
    *,
    async_session: AsyncSession,
    user_id: int,
    slug: str,
    address: str,
) -> Url:
    """Create a new url and commit it to the database.

    Args:
        async_session (AsyncSession): The database session.
        user_id (int): The ` id ` of the user that owns new url.
        slug (str): The short URL address.
        address (str): The long URL address.

    Returns:
        The newly created ` Url ` instance.
    """
    url: Url = Url(
        user_id=user_id,
        slug=slug,
        address=address,
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
    """Retrieve a ` Url ` by its slug.

    Args:
        async_session (AsyncSession): The database session.
        slug (str): The slug of the ` Url `.

    Returns:
        The ` Url ` instance if found, otherwise ` None `.
    """
    result: Result[tuple[Url]] = await async_session.execute(
        select(Url).filter(Url.slug == slug),
    )
    url: Url | None = result.scalars().first()

    return url


async def get_urls_by_page_and_limit(
    *,
    async_session: AsyncSession,
    page: int,
    limit: int,
) -> list[Url]:
    """Retrieve a paginated and sorted list of ` Url `.

    Args:
        async_session (AsyncSession): The database session.
        page (int): The page number.
        limit (int): The number of records per page.

    Returns:
        A list of ` Url ` records for the requested page.
    """
    result: Result[tuple[Url]] = await async_session.execute(
        select(Url)
        .order_by(desc(Url.created_at))
        .offset((page - 1) * limit)
        .limit(limit),
    )
    urls: list[Url] = list(result.scalars().all())

    return urls


async def update_url(
    *,
    async_session: AsyncSession,
    url: Url,
    slug: str | None = None,
    address: str | None = None,
    total_clicks: int | None = None,
) -> Url:
    """Update the ` Url ` attributes with the given values.

    Args:
        async_session (AsyncSession): The database session.
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

    async_session.add(url)
    await async_session.commit()
    await async_session.refresh(url)
    return url
