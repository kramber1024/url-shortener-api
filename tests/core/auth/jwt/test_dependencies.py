import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth.jwt import (
    generate_token,
    get_current_user,
    get_refreshed_user,
)
from app.core.database.models import User
from app.core.settings import settings


@pytest.fixture()
def access_token(user: User, current_time: int) -> str:
    return generate_token(
        "access",
        user_id=user.id,
        email=user.email,
        key=settings.jwt.SECRET,
        current_time=current_time,
    )


@pytest.fixture()
def refresh_token(user: User, current_time: int) -> str:
    return generate_token(
        "refresh",
        user_id=user.id,
        email=user.email,
        key=settings.jwt.SECRET,
        current_time=current_time,
    )


@pytest.mark.asyncio()
async def test_get_current_user(
    async_session: AsyncSession,
    access_token: str | None,
    user: User,
) -> None:
    current_user: User = await get_current_user(async_session, access_token)

    assert current_user.id == user.id
    assert current_user.email == user.email


@pytest.mark.asyncio()
async def test_get_current_user_no_token(
    async_session: AsyncSession,
) -> None:
    with pytest.raises(HTTPException):
        await get_current_user(async_session, None)


@pytest.mark.asyncio()
async def test_get_current_user_invalid_token(
    async_session: AsyncSession,
) -> None:
    with pytest.raises(HTTPException):
        await get_current_user(async_session, "invalid_token")


@pytest.mark.asyncio()
async def test_get_current_user_no_user(
    async_session: AsyncSession,
    current_time: int,
    user: User,
) -> None:
    access_token: str = generate_token(
        "access",
        user_id=user.id + 1,
        email=user.email,
        key=settings.jwt.SECRET,
        current_time=current_time,
    )

    with pytest.raises(HTTPException):
        await get_current_user(async_session, access_token)


@pytest.mark.asyncio()
async def test_get_refreshed_user(
    async_session: AsyncSession,
    refresh_token: str | None,
    user: User,
) -> None:
    refreshed_user: User = await get_refreshed_user(
        async_session,
        refresh_token,
    )

    assert refreshed_user.id == user.id
    assert refreshed_user.email == user.email


@pytest.mark.asyncio()
async def test_get_refreshed_user_no_token(
    async_session: AsyncSession,
) -> None:
    with pytest.raises(HTTPException):
        await get_refreshed_user(async_session, None)


@pytest.mark.asyncio()
async def test_get_refreshed_user_invalid_token(
    async_session: AsyncSession,
) -> None:
    with pytest.raises(HTTPException):
        await get_refreshed_user(async_session, "invalid_token")


@pytest.mark.asyncio()
async def test_get_refreshed_user_no_user(
    async_session: AsyncSession,
    current_time: int,
    user: User,
) -> None:
    refresh_token: str = generate_token(
        "refresh",
        user_id=user.id + 1,
        email=user.email,
        key=settings.jwt.SECRET,
        current_time=current_time,
    )

    with pytest.raises(HTTPException):
        await get_refreshed_user(async_session, refresh_token)
