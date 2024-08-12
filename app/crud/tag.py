from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Tag


async def create_tag(
    *,
    session: AsyncSession,
    url_id: int,
    name: str,
) -> Tag:
    tag: Tag = Tag(
        url_id=url_id,
        name=name,
    )

    session.add(tag)
    await session.commit()
    await session.refresh(tag)
    return tag
