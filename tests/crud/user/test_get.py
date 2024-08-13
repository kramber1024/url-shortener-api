import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database.models import User
from tests import utils


@pytest.mark.asyncio
async def test_get_user_by_email(
    session: AsyncSession,
    db_user: User,
) -> None:
    user: User | None = await crud.get_user_by_email(
        session=session,
        email=db_user.email,
    )

    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == db_user.first_name
    assert user.last_name == db_user.last_name
    assert user.email == db_user.email
    assert not user.phone
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status
    assert user.status.user_id == db_user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium
    assert not user.urls


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(
    session: AsyncSession,
    db_user: User,
) -> None:
    user: User | None = await crud.get_user_by_email(
        session=session,
        email=db_user.email[::-1],
    )

    assert not user


@pytest.mark.asyncio
async def test_get_user_by_id(
    session: AsyncSession,
    db_user: User,
) -> None:
    user: User | None = await crud.get_user_by_id(
        session=session,
        id_=db_user.id,
    )

    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == db_user.first_name
    assert user.last_name == db_user.last_name
    assert user.email == db_user.email
    assert not user.phone
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status
    assert user.status.user_id == db_user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium
    assert not user.urls


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(
    session: AsyncSession,
    db_user: User,
) -> None:
    user: User | None = await crud.get_user_by_id(
        session=session,
        id_=db_user.id - 1,
    )

    assert not user
