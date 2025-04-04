import pytest
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database.models import Status


@pytest.fixture(scope="module")
def user_id() -> int:
    return 1


@pytest.mark.asyncio()
@pytest.mark.parametrize(("active"), [True, False])
async def test_create_status(
    async_session: AsyncSession,
    user_id: int,
    active: bool,
) -> None:
    status: Status = await crud.create_status(
        async_session=async_session,
        user_id=user_id,
        active=active,
    )

    result: Result[tuple[Status]] = await async_session.execute(
        select(Status).where(Status.user_id == user_id),
    )
    database_status: Status | None = result.scalars().first()
    assert database_status
    assert database_status.user_id == status.user_id
    assert database_status.active == status.active
    assert database_status.email_verified == status.email_verified
    assert database_status.phone_verified == status.phone_verified
