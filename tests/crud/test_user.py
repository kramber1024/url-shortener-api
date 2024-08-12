import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database.models import User
from tests import utils


@pytest.mark.asyncio
async def test_create_user(
    session: AsyncSession,
) -> None:
    first_name: str = "Brenda"
    last_name: str = "Reichel"
    email: str = "Terrill90@gmail.com"
    password: str = "uoqaEB344$#@uuc123$$$.-_==1&77**991239%$#@!455ANcqxdPPNcqxdcAcqx"

    user: User = await crud.create_user(
        session=session,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == email
    assert user.phone is None
    assert user.password != password
    assert user.is_password_valid(password)


@pytest.mark.asyncio
async def test_create_user_uppercase(
    session: AsyncSession,
) -> None:
    first_name: str = "Teagan".upper()
    last_name: str = "Reichel".upper()
    email: str = "Terrill90@gmail.com".upper()
    password: str = "u44$#@uuc123$$$.-_==1&77**991239%$#@!455ANcqxdPPNcqxdcAcqx".upper()

    user: User = await crud.create_user(
        session=session,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == utils.format_email(email)
    assert user.phone is None
    assert user.password != password
    assert user.is_password_valid(password)


@pytest.mark.asyncio
async def test_create_user_empty(
    session: AsyncSession,
) -> None:
    first_name: str = ""
    email: str = ""
    password: str = ""

    user: User = await crud.create_user(
        session=session,
        first_name=first_name,
        last_name=None,
        email=email,
        password=password,
    )

    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == first_name
    assert user.last_name is None
    assert user.email == email
    assert user.phone is None
    assert user.password != password
    assert user.is_password_valid("")


@pytest.mark.asyncio
async def test_get_user_by_email(
    session: AsyncSession,
    db_user: User,
) -> None:
    user: User | None = await crud.get_user_by_email(
        session=session,
        email=db_user.email,
    )

    assert user is not None
    assert user.id == db_user.id
    assert user.first_name == db_user.first_name
    assert user.last_name == db_user.last_name
    assert user.email == db_user.email
    assert user.phone == db_user.phone
    assert user.password == db_user.password
    assert user.is_password_valid(utils.USER_PASSWORD)


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(
    session: AsyncSession,
    db_user: User,
) -> None:
    user: User | None = await crud.get_user_by_email(
        session=session,
        email=db_user.email[::-1],
    )

    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_id(
    session: AsyncSession,
    db_user: User,
) -> None:
    user: User | None = await crud.get_user_by_id(
        session=session,
        id_=db_user.id,
    )

    assert user is not None
    assert user.id == db_user.id
    assert user.first_name == db_user.first_name
    assert user.last_name == db_user.last_name
    assert user.email == db_user.email
    assert user.phone == db_user.phone
    assert user.password == db_user.password
    assert user.is_password_valid(utils.USER_PASSWORD)


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(
    session: AsyncSession,
    db_user: User,
) -> None:
    user: User | None = await crud.get_user_by_id(
        session=session,
        id_=db_user.id - 1,
    )

    assert user is None
