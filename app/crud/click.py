from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Click


async def create_click(
    *,
    async_session: AsyncSession,
    url_id: int,
    ip: str | None,
    country: str | None,
) -> Click:
    """Initialize a new ` Click ` and commit it to the database.

    Args:
        async_session: The async database session.
        url_id: The unique identifier of the ` Url `.
        ip: The IP address from which the ` Click ` was made.
        country: The two-letter country code of the origin of the ` Click `.

    Returns:
        The newly created ` Click ` instance.
    """
    click: Click = Click(
        url_id=url_id,
        ip=ip,
        country=country,
    )

    async_session.add(click)
    await async_session.commit()
    await async_session.refresh(click)

    return click
