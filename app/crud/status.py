from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Status


async def create_status(
    *,
    session: AsyncSession,
    user_id: int,
    active: bool,
    premium: bool,
) -> Status:
    status: Status = Status(
        user_id=user_id,
        active=active,
        premium=premium,
    )

    session.add(status)
    await session.commit()
    await session.refresh(status)
    return status
