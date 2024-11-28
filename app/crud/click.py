from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Click


async def create_click(
    *,
    async_session: AsyncSession,
    url_id: int,
    ip: str | None,
    country: str | None,
) -> Click:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    async_session.add(click)
    await async_session.commit()
    await async_session.refresh(click)
    return click
