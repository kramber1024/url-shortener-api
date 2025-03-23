from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Status


async def create_status(
    *,
    async_session: AsyncSession,
    user_id: int,
    active: bool,
) -> Status:
    """Initialize a new ` Status ` and commit it to the database.

    Args:
        async_session: The async database session.
        user_id: The unique identifier of the ` User `.
        active: Indicates whether the ` User ` is currently active.

    Returns:
        The newly created ` Status ` instance.
    """
    status: Status = Status(
        user_id=user_id,
        active=active,
    )

    async_session.add(status)
    await async_session.commit()
    await async_session.refresh(status)

    return status
