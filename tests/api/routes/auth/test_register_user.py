from typing import TYPE_CHECKING

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database.models import User
from tests import utils

if TYPE_CHECKING:
    from httpx import Response
    from sqlalchemy.engine import Result

    from tests.api.types_ import Json


@pytest.mark.asyncio()
async def test_register_user(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": user_credentials.first_name,
        "last_name": str(user_credentials.last_name),
        "email": user_credentials.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(user_credentials.email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_201_CREATED
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name
    assert user.last_name == user_credentials.last_name
    assert user.email == user_credentials.email
    assert not user.phone
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium
    assert not user.urls


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    (
        "first_name",
        "validated_first_name",
    ),
    [
        ("a" * settings.data.FIRST_NAME_MIN_LENGTH,) * 2,
        ("a" * settings.data.FIRST_NAME_MAX_LENGTH,) * 2,
        ("A" * settings.data.FIRST_NAME_MAX_LENGTH,) * 2,
        ("  aaa", "aaa"),
        ("aaa  ", "aaa"),
        ("  aaa  ", "aaa"),
    ],
)
async def test_register_user_first_name(
    first_name: str,
    validated_first_name: str,
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": first_name,
        "last_name": user_credentials.last_name,
        "email": user_credentials.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(user_credentials.email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_201_CREATED
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == validated_first_name
    assert user.last_name == user_credentials.last_name
    assert user.email == user_credentials.email
    assert not user.phone
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium
    assert not user.urls


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    (
        "last_name",
        "validated_last_name",
    ),
    [
        ("a" * settings.data.LAST_NAME_MIN_LENGTH,) * 2,
        ("a" * settings.data.LAST_NAME_MAX_LENGTH,) * 2,
        ("A" * settings.data.LAST_NAME_MAX_LENGTH,) * 2,
        ("  aaa", "aaa"),
        ("aaa  ", "aaa"),
        ("  aaa  ", "aaa"),
        (None,) * 2,
    ],
)
async def test_register_user_last_name(
    last_name: str | None,
    validated_last_name: str | None,
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": user_credentials.first_name,
        "email": user_credentials.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    if last_name:
        json["last_name"] = last_name

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(user_credentials.email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_201_CREATED
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name
    assert user.last_name == validated_last_name
    assert user.email == user_credentials.email
    assert not user.phone
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium
    assert not user.urls


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    (
        "email",
        "validated_email",
    ),
    [
        ("a" * (settings.data.EMAIL_MAX_LENGTH - len("@b.c")) + "@b.c",) * 2,
        ("A" * (settings.data.EMAIL_MAX_LENGTH - len("@b.c")) + "@b.c",) * 2,
        ("email@EXAMPLE.COM", "email@example.com"),
        ("a.a.a.a@b.c",) * 2,
    ],
)
async def test_register_user_email(
    email: str,
    validated_email: str,
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": user_credentials.first_name,
        "last_name": user_credentials.last_name,
        "email": email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == validated_email),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_201_CREATED
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name
    assert user.last_name == user_credentials.last_name
    assert user.email == validated_email
    assert not user.phone
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium
    assert not user.urls


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "password",
    [
        "a" * settings.data.PASSWORD_MIN_LENGTH,
        "a" * settings.data.PASSWORD_MAX_LENGTH,
        "A" * settings.data.PASSWORD_MAX_LENGTH,
    ],
)
async def test_register_user_password(
    password: str,
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": user_credentials.first_name,
        "last_name": user_credentials.last_name,
        "email": user_credentials.email,
        "password": password,
        "terms": "on",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(user_credentials.email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_201_CREATED
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name
    assert user.last_name == user_credentials.last_name
    assert user.email == user_credentials.email
    assert not user.phone
    assert user.password != password
    assert user.is_password_valid(password)
    assert user.status
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium
    assert not user.urls


@pytest.mark.asyncio()
async def test_register_user_terms(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": user_credentials.first_name,
        "last_name": user_credentials.last_name,
        "email": user_credentials.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(user_credentials.email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_201_CREATED
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name
    assert user.last_name == user_credentials.last_name
    assert user.email == user_credentials.email
    assert not user.phone
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium
    assert not user.urls


@pytest.mark.asyncio()
async def test_register_user_email_conflict(
    session: AsyncSession,
    client: AsyncClient,
    db_user: User,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": user_credentials.first_name,
        "email": db_user.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(db_user.email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_409_CONFLICT
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name
    assert user.last_name == user_credentials.last_name
    assert user.email == user_credentials.email
    assert not user.phone
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium
    assert not user.urls


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "first_name",
    [
        "",
        " " * settings.data.FIRST_NAME_MIN_LENGTH,
        "a" * (settings.data.FIRST_NAME_MIN_LENGTH - 1),
        "a" * (settings.data.FIRST_NAME_MAX_LENGTH + 1),
    ],
)
async def test_register_user_invalid_first_name(
    first_name: str,
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": first_name,
        "email": user_credentials.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(user_credentials.email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == 1
    assert utils.error_type_exists(response.json(), "first_name")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not user


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "last_name",
    [
        "",
        " " * settings.data.LAST_NAME_MIN_LENGTH,
        "a" * (settings.data.LAST_NAME_MIN_LENGTH - 1),
        "a" * (settings.data.LAST_NAME_MAX_LENGTH + 1),
    ],
)
async def test_register_user_invalid_last_name(
    last_name: str,
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": user_credentials.first_name,
        "last_name": last_name,
        "email": user_credentials.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(user_credentials.email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == 1
    assert utils.error_type_exists(response.json(), "last_name")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not user


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "email",
    [
        "",
        "a" * (settings.data.EMAIL_MAX_LENGTH + 1),
        "@a.b",
        "a@b",
        "@a",
        "a@",
        "a" * (settings.data.EMAIL_MAX_LENGTH - len("@b.c") + 1) + "@b.c",
    ],
)
async def test_register_user_invalid_email(
    email: str,
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": user_credentials.first_name,
        "email": email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == 1
    assert utils.error_type_exists(response.json(), "email")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not user


@pytest.mark.asyncio()
@pytest.mark.parametrize(
    "password",
    [
        "",
        " " * (settings.data.PASSWORD_MAX_LENGTH + 1),
        "a" * (settings.data.PASSWORD_MIN_LENGTH - 1),
        "a" * (settings.data.PASSWORD_MAX_LENGTH + 1),
    ],
)
async def test_register_user_invalid_password(
    password: str,
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": user_credentials.first_name,
        "email": user_credentials.email,
        "password": password,
        "terms": "on",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(user_credentials.email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == 1
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not user


@pytest.mark.asyncio()
async def test_register_user_invalid_terms(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: Json = {
        "first_name": user_credentials.first_name,
        "email": user_credentials.email,
        "password": user_credentials.password,
        "terms": "off",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == user_credentials.email),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == 1
    assert utils.error_type_exists(response.json(), "terms")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not user


@pytest.mark.asyncio()
async def test_register_user_invalid_all(
    session: AsyncSession,
    client: AsyncClient,
) -> None:
    invalid_email: str = (
        "a" * (settings.data.EMAIL_MAX_LENGTH - len("@b.c") + 1) + "@b.c"
    )

    json: Json = {
        "first_name": "a" * (settings.data.FIRST_NAME_MAX_LENGTH + 1),
        "last_name": "a" * (settings.data.LAST_NAME_MAX_LENGTH + 1),
        "email": invalid_email,
        "password": "a" * (settings.data.PASSWORD_MAX_LENGTH + 1),
        "terms": "off",
    }

    response: Response = await client.post(
        "/api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(invalid_email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == len(
        [
            "first_name",
            "last_name",
            "email",
            "password",
            "terms",
        ],
    )
    assert utils.error_type_exists(response.json(), "first_name")
    assert utils.error_type_exists(response.json(), "last_name")
    assert utils.error_type_exists(response.json(), "email")
    assert utils.error_type_exists(response.json(), "password")
    assert utils.error_type_exists(response.json(), "terms")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not user


@pytest.mark.asyncio()
async def test_register_user_empty(
    session: AsyncSession,
    client: AsyncClient,
) -> None:
    empty_email: str = ""

    response: Response = await client.post(
        "api/auth/register",
        json={},
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == empty_email),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == len(
        [
            "first_name",
            "email",
            "password",
            "terms",
        ],
    )
    assert utils.error_type_exists(response.json(), "first_name")
    assert utils.error_type_exists(response.json(), "email")
    assert utils.error_type_exists(response.json(), "password")
    assert utils.error_type_exists(response.json(), "terms")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert not user
