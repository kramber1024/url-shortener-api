import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database.models import User
from tests import testing_utils


@pytest.mark.asyncio
async def test_create_user(
    session: AsyncSession,
    user_credentials: User,
) -> None:
    user: User = await crud.create_user(
        session=session,
        first_name=user_credentials.first_name,
        last_name=user_credentials.last_name,
        email=user_credentials.email,
        password=testing_utils.USER_PASSWORD,
    )

    assert user
    assert user.id in testing_utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name
    assert user.last_name == user_credentials.last_name
    assert user.email == user_credentials.email
    assert not user.phone
    assert user.password != testing_utils.USER_PASSWORD
    assert user.is_password_valid(testing_utils.USER_PASSWORD)
    assert user.updated_at
    assert user.created_at
    assert not user.status
    assert not user.urls


@pytest.mark.asyncio
async def test_create_user_two_in_a_row(
    session: AsyncSession,
    user_credentials: User,
) -> None:
    user_1: User = await crud.create_user(
        session=session,
        first_name=user_credentials.first_name,
        last_name=user_credentials.last_name,
        email=user_credentials.email,
        password=testing_utils.USER_PASSWORD,
    )

    user_2: User = await crud.create_user(
        session=session,
        first_name=user_credentials.first_name,
        last_name=user_credentials.last_name,
        email=user_credentials.email + "ma",
        password=testing_utils.USER_PASSWORD,
    )

    assert user_1
    assert user_1.id in testing_utils.SNOWFLAKE_RANGE
    assert user_1.first_name == user_credentials.first_name
    assert user_1.last_name == user_credentials.last_name
    assert user_1.email == user_credentials.email
    assert not user_1.phone
    assert user_1.password != testing_utils.USER_PASSWORD
    assert user_1.is_password_valid(testing_utils.USER_PASSWORD)
    assert user_1.updated_at
    assert user_1.created_at
    assert not user_1.status
    assert not user_1.urls
    assert user_2
    assert user_2.id in testing_utils.SNOWFLAKE_RANGE
    assert user_2.first_name == user_credentials.first_name
    assert user_2.last_name == user_credentials.last_name
    assert user_2.email == user_credentials.email + "ma"
    assert not user_2.phone
    assert user_2.password != testing_utils.USER_PASSWORD
    assert user_2.is_password_valid(testing_utils.USER_PASSWORD)
    assert user_2.updated_at
    assert user_2.created_at
    assert not user_2.status
    assert not user_2.urls


@pytest.mark.asyncio
async def test_create_user_no_last_name(
    session: AsyncSession,
    user_credentials: User,
) -> None:
    user: User = await crud.create_user(
        session=session,
        first_name=user_credentials.first_name,
        last_name=None,
        email=user_credentials.email,
        password=testing_utils.USER_PASSWORD,
    )

    assert user
    assert user.id in testing_utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name
    assert not user.last_name
    assert user.email == user_credentials.email
    assert not user.phone
    assert user.password != testing_utils.USER_PASSWORD
    assert user.is_password_valid(testing_utils.USER_PASSWORD)
    assert user.updated_at
    assert user.created_at
    assert not user.status
    assert not user.urls


@pytest.mark.asyncio
async def test_create_user_uppercase(
    session: AsyncSession,
    user_credentials: User,
) -> None:
    user: User = await crud.create_user(
        session=session,
        first_name=user_credentials.first_name.upper(),
        last_name=str(user_credentials.last_name).upper(),
        email=user_credentials.email.upper(),
        password=testing_utils.USER_PASSWORD.upper(),
    )

    assert user
    assert user.id in testing_utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name.upper()
    assert user.last_name == str(user_credentials.last_name).upper()
    assert user.email == testing_utils.format_email(
        user_credentials.email.upper(),
    )
    assert not user.phone
    assert user.password != testing_utils.USER_PASSWORD.upper()
    assert user.is_password_valid(testing_utils.USER_PASSWORD.upper())
    assert user.updated_at
    assert user.created_at
    assert not user.status
    assert not user.urls


@pytest.mark.asyncio
async def test_create_user_empty(
    session: AsyncSession,
) -> None:
    user: User = await crud.create_user(
        session=session,
        first_name="",
        last_name=None,
        email="",
        password="",
    )

    assert user
    assert user.id in testing_utils.SNOWFLAKE_RANGE
    assert not user.first_name
    assert not user.last_name
    assert not user.email
    assert not user.phone
    assert user.password
    assert user.is_password_valid("")
    assert user.updated_at
    assert user.created_at
    assert not user.status
    assert not user.urls


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
    assert user
    assert user.id in testing_utils.SNOWFLAKE_RANGE
    assert user.first_name == db_user.first_name
    assert user.last_name == db_user.last_name
    assert user.email == db_user.email
    assert not user.phone
    assert user.password != testing_utils.USER_PASSWORD
    assert user.is_password_valid(testing_utils.USER_PASSWORD)
    assert user.updated_at
    assert user.created_at
    assert user.status
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
        user_id=db_user.id,
    )

    assert user
    assert user
    assert user.id in testing_utils.SNOWFLAKE_RANGE
    assert user.first_name == db_user.first_name
    assert user.last_name == db_user.last_name
    assert user.email == db_user.email
    assert not user.phone
    assert user.password != testing_utils.USER_PASSWORD
    assert user.is_password_valid(testing_utils.USER_PASSWORD)
    assert user.updated_at
    assert user.created_at
    assert user.status
    assert not user.urls


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(
    session: AsyncSession,
    db_user: User,
) -> None:
    user: User | None = await crud.get_user_by_id(
        session=session,
        user_id=db_user.id - 1,
    )

    assert not user
