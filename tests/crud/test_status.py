from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud

if TYPE_CHECKING:
    from app.core.database.models import Status


@pytest.mark.asyncio
async def test_create_status(
    session: AsyncSession,
) -> None:

    id_: int = 11231231234124

    status: Status = await crud.create_status(
        session=session,
        user_id=id_,
    )

    assert status.user_id == id_
    assert status.email_verified is False
    assert status.phone_verified is False
    assert status.active is True
    assert status.premium is False


@pytest.mark.asyncio
async def test_create_status_inactive(
    session: AsyncSession,
) -> None:

    id_: int = 5124124124124124

    status: Status = await crud.create_status(
        session=session,
        user_id=id_,
        active=False,
    )

    assert status.user_id == id_
    assert status.email_verified is False
    assert status.phone_verified is False
    assert status.active is False
    assert status.premium is False


@pytest.mark.asyncio
async def test_create_status_premium(
    session: AsyncSession,
) -> None:

    id_: int = 5124124124124124

    status: Status = await crud.create_status(
        session=session,
        user_id=id_,
        premium=True,
    )

    assert status.user_id == id_
    assert status.email_verified is False
    assert status.phone_verified is False
    assert status.active is True
    assert status.premium is True
