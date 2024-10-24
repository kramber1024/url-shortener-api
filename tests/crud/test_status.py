from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database.models import User

if TYPE_CHECKING:
    from app.core.database.models import Status


@pytest.mark.asyncio
async def test_create_status(
    session: AsyncSession,
    user_credentials: User,
) -> None:
    status: Status = await crud.create_status(
        session=session,
        user_id=user_credentials.id,
        active=True,
        premium=False,
    )

    assert status
    assert status.user_id == user_credentials.id
    assert not status.email_verified
    assert not status.phone_verified
    assert status.active
    assert not status.premium


@pytest.mark.asyncio
async def test_create_status_inactive(
    session: AsyncSession,
    user_credentials: User,
) -> None:
    status: Status = await crud.create_status(
        session=session,
        user_id=user_credentials.id,
        active=False,
        premium=False,
    )

    assert status
    assert status.user_id == user_credentials.id
    assert not status.email_verified
    assert not status.phone_verified
    assert not status.active
    assert not status.premium


@pytest.mark.asyncio
async def test_create_status_premium(
    session: AsyncSession,
    user_credentials: User,
) -> None:
    status: Status = await crud.create_status(
        session=session,
        user_id=user_credentials.id,
        active=True,
        premium=True,
    )

    assert status
    assert status.user_id == user_credentials.id
    assert not status.email_verified
    assert not status.phone_verified
    assert status.active
    assert status.premium
