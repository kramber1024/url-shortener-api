import pytest
import pytest_asyncio
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database.models import User


@pytest.fixture(scope="module")
def first_name() -> str:
    return "John"


@pytest.fixture(scope="module")
def last_name() -> str:
    return "Doe"


@pytest.fixture(scope="module")
def email() -> str:
    return "john.doe@example.com"


@pytest.fixture(scope="module")
def password() -> str:
    return "securepassword"


@pytest_asyncio.fixture()
async def user(
    async_session: AsyncSession,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
) -> User:
    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    async_session.add(user)
    await async_session.commit()

    return user


@pytest.mark.asyncio()
async def test_create_user(
    async_session: AsyncSession,
    first_name: str,
    last_name: str,
    email: str,
    password: str,
) -> None:
    user: User = await crud.create_user(
        async_session=async_session,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    result: Result[tuple[User]] = await async_session.execute(
        select(User).where(User.email == email),
    )
    database_user: User | None = result.scalars().first()
    assert database_user
    assert database_user.first_name == user.first_name
    assert database_user.last_name == user.last_name
    assert database_user.email == user.email


@pytest.mark.asyncio()
async def test_get_user_by_id(
    async_session: AsyncSession,
    user: User,
) -> None:
    database_user: User | None = await crud.get_user_by_id(
        async_session=async_session,
        user_id=user.id,
    )

    assert database_user is not None
    assert database_user.id == user.id


@pytest.mark.asyncio()
async def test_get_user_by_id_not_found(
    async_session: AsyncSession,
    user: User,
) -> None:
    database_user: User | None = await crud.get_user_by_id(
        async_session=async_session,
        user_id=user.id + 1,
    )

    assert database_user is None


@pytest.mark.asyncio()
async def test_get_user_by_email(
    async_session: AsyncSession,
    user: User,
) -> None:
    database_user: User | None = await crud.get_user_by_email(
        async_session=async_session,
        email=user.email,
    )

    assert database_user is not None
    assert database_user.email == user.email


@pytest.mark.asyncio()
async def test_get_user_by_email_not_found(
    async_session: AsyncSession,
    user: User,
) -> None:
    database_user: User | None = await crud.get_user_by_email(
        async_session=async_session,
        email=user.email[::-1],
    )

    assert database_user is None
