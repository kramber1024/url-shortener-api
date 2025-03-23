from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Tag


async def create_tag(
    *,
    async_session: AsyncSession,
    url_id: int,
    name: str,
) -> Tag:
    """Initialize a new ` Tag ` and commit it to the database.

    Args:
        async_session: The async database session.
        url_id: The unique identifier of the ` Url `.
        name: The ` Tag ` value.

    Returns:
        The newly created ` Tag ` instance.
    """
    tag: Tag = Tag(
        url_id=url_id,
        name=name,
    )

    async_session.add(tag)
    await async_session.commit()
    await async_session.refresh(tag)

    return tag
