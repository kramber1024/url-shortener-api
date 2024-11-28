from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Tag


async def create_tag(
    *,
    async_session: AsyncSession,
    url_id: int,
    name: str,
) -> Tag:
    tag: Tag = Tag(
        url_id=url_id,
        name=name,
    )

    async_session.add(tag)
    await async_session.commit()
    await async_session.refresh(tag)
    return tag
