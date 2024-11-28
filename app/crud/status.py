from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Status


async def create_status(
    *,
    async_session: AsyncSession,
    user_id: int,
    active: bool,
    premium: bool,
) -> Status:
    status: Status = Status(
        user_id=user_id,
        active=active,
        premium=premium,
    )

    async_session.add(status)
    await async_session.commit()
    await async_session.refresh(status)
    return status
