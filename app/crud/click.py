from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Click


async def create_click(
    *,
    session: AsyncSession,
    url_id: int,
    ip: str | None,
    country: str | None,
) -> Click:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    session.add(click)
    await session.commit()
    await session.refresh(click)
    return click
