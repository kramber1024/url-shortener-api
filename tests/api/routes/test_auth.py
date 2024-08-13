from typing import TYPE_CHECKING

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import jwt_
from app.core.database.models import User
from tests import utils

if TYPE_CHECKING:
    from httpx import Response
    from sqlalchemy.engine import Result


@pytest.mark.asyncio()
async def test_register_user(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: dict[str, str] = {
        "first_name": user_credentials.first_name,
        "last_name": str(user_credentials.last_name),
        "email": user_credentials.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == user_credentials.email),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_201_CREATED
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name
    assert user.last_name == user_credentials.last_name
    assert user.email == user_credentials.email
    assert user.phone is None
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium


@pytest.mark.asyncio()
async def test_register_user_no_last_name(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: dict[str, str] = {
        "first_name": user_credentials.first_name,
        "email": user_credentials.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == user_credentials.email),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_201_CREATED
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == user_credentials.first_name
    assert user.last_name is None
    assert user.email == user_credentials.email
    assert user.phone is None
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium


@pytest.mark.asyncio()
async def test_register_user_uppercase(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    first_name: str = user_credentials.first_name.upper()
    last_name: str = str(user_credentials.last_name).upper()
    email: str = user_credentials.email.upper()
    password: str = utils.USER_PASSWORD.upper()

    json: dict[str, str] = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "terms": "on",
    }

    response: Response = await client.post(
        "api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_201_CREATED
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == utils.format_email(email)
    assert user.phone is None
    assert user.password != password
    assert user.is_password_valid(password)
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium


@pytest.mark.asyncio()
async def test_register_user_email_conflict(
    session: AsyncSession,
    client: AsyncClient,
    db_user: User,
    user_credentials: User,
) -> None:
    json: dict[str, str] = {
        "first_name": user_credentials.first_name,
        "email": db_user.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(db_user.email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_409_CONFLICT
    assert len(response.json().get("errors", [0])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_409_CONFLICT
    assert user
    assert user.id in utils.SNOWFLAKE_RANGE
    assert user.first_name == db_user.first_name
    assert user.last_name == db_user.last_name
    assert user.email == db_user.email
    assert user.phone is None
    assert user.password != utils.USER_PASSWORD
    assert user.is_password_valid(utils.USER_PASSWORD)
    assert user.status.user_id == user.id
    assert not user.status.email_verified
    assert not user.status.phone_verified
    assert user.status.active
    assert not user.status.premium


@pytest.mark.asyncio()
async def test_register_user_invalid_first_name(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: dict[str, str] = {
        "first_name": "Hi",
        "email": user_credentials.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == user_credentials.email),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == 1
    assert utils.error_type_exists(response.json(), "first_name")
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert user is None


@pytest.mark.asyncio()
async def test_register_user_invalid_last_name(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: dict[str, str] = {
        "first_name": user_credentials.first_name,
        "last_name": "Hi",
        "email": user_credentials.email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == user_credentials.email),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == 1
    assert utils.error_type_exists(response.json(), "last_name")
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert user is None


@pytest.mark.asyncio()
async def test_register_user_invalid_email(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    invalid_email: str = "a@a."

    json: dict[str, str] = {
        "first_name": user_credentials.first_name,
        "email": invalid_email,
        "password": utils.USER_PASSWORD,
        "terms": "on",
    }

    response: Response = await client.post(
        "api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(invalid_email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == 1
    assert utils.error_type_exists(response.json(), "email")
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert user is None


@pytest.mark.asyncio()
async def test_register_user_invalid_password(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: dict[str, str] = {
        "first_name": user_credentials.first_name,
        "email": user_credentials.email,
        "password": "123",
        "terms": "on",
    }

    response: Response = await client.post(
        "api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == user_credentials.email),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == 1
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert user is None


@pytest.mark.asyncio()
async def test_register_user_invalid_terms(
    session: AsyncSession,
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: dict[str, str] = {
        "first_name": user_credentials.first_name,
        "email": user_credentials.email,
        "password": user_credentials.password,
        "terms": "off",
    }

    response: Response = await client.post(
        "api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == user_credentials.email),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == 1
    assert utils.error_type_exists(response.json(), "terms")
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert user is None


@pytest.mark.asyncio()
async def test_register_user_invalid_all(
    session: AsyncSession,
    client: AsyncClient,
) -> None:
    invalid_first_name: str = "26"
    invalid_last_name: str = "26"
    invalid_email: str = "26"
    invalid_password: str = "26"

    json: dict[str, str] = {
        "first_name": invalid_first_name,
        "last_name": invalid_last_name,
        "email": invalid_email,
        "password": invalid_password,
        "terms": "26",
    }

    response: Response = await client.post(
        "api/auth/register",
        json=json,
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == utils.format_email(invalid_email)),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == len(
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
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert user is None


@pytest.mark.asyncio()
async def test_register_user_empty(
    session: AsyncSession,
    client: AsyncClient,
) -> None:
    email: str = ""

    response: Response = await client.post(
        "api/auth/register",
        json={},
    )

    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == email),
    )
    user: User | None = result.scalars().first()

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == len(
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
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert user is None


@pytest.mark.asyncio()
async def test_authenticate_user(
    client: AsyncClient,
    db_user: User,
) -> None:
    json: dict[str, str] = {
        "email": db_user.email,
        "password": utils.USER_PASSWORD,
    }

    response: Response = await client.post(
        "api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_200_OK
    assert response.cookies.get("access_token", "")
    assert response.cookies.get("refresh_token", "")


@pytest.mark.asyncio()
async def test_authenticate_user_incorrect_email(
    client: AsyncClient,
    db_user: User,
) -> None:
    json: dict[str, str] = {
        "email": db_user.email + "a",
        "password": utils.USER_PASSWORD,
    }

    response: Response = await client.post(
        "api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", [0])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_401_UNAUTHORIZED
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")


@pytest.mark.asyncio()
async def test_authenticate_user_incorrect_password(
    client: AsyncClient,
    db_user: User,
) -> None:
    json: dict[str, str] = {
        "email": db_user.email,
        "password": utils.USER_PASSWORD[::-1],
    }

    response: Response = await client.post(
        "api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", [0])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_401_UNAUTHORIZED
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")


@pytest.mark.asyncio()
async def test_authenticate_user_incorrect_all(
    client: AsyncClient,
    db_user: User,
) -> None:
    json: dict[str, str] = {
        "email": db_user.email + "a",
        "password": utils.USER_PASSWORD[::-1],
    }

    response: Response = await client.post(
        "api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", [0])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_401_UNAUTHORIZED
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")


@pytest.mark.asyncio()
async def test_authenticate_user_invalid_email(
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: dict[str, str] = {
        "email": "........",
        "password": user_credentials.password,
    }

    response: Response = await client.post(
        "api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == 1
    assert utils.error_type_exists(response.json(), "email")
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_authenticate_user_invalid_password(
    client: AsyncClient,
    user_credentials: User,
) -> None:
    json: dict[str, str] = {
        "email": user_credentials.email,
        "password": "12345",
    }

    response: Response = await client.post(
        "api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == 1
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_authenticate_user_invalid_all(
    client: AsyncClient,
) -> None:
    json: dict[str, str] = {
        "email": "...",
        "password": "...",
    }

    response: Response = await client.post(
        "api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == len(["email", "password"])
    assert utils.error_type_exists(response.json(), "email")
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_authenticate_user_empty(
    client: AsyncClient,
) -> None:
    response: Response = await client.post(
        "api/auth/login",
        json={},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [0])) == len(["email", "password"])
    assert utils.error_type_exists(response.json(), "email")
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio()
async def test_refresh_user(
    client: AsyncClient,
    db_user: User,
) -> None:
    refresh_token: str = jwt_.generate_refresh_token(
        user_id=db_user.id,
        email=db_user.email,
    )

    client.cookies.set("refresh_token", refresh_token)
    response: Response = await client.post(
        "api/auth/refresh",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_200_OK
    assert response.cookies.get("access_token", "")
    assert response.cookies.get("refresh_token", "")


@pytest.mark.asyncio()
async def test_refresh_user_incorrect_token(
    client: AsyncClient,
) -> None:
    refresh_token: str = (
        "wnce8OakjfsPgNSWvlZosGgSWkXPhR."
        "19Q5n3vX04pJorG6Ps2LYzrmZr1Xdc."
        "fO43J2Amatx31wE9iLUDFcxm08KPva"
    )

    client.cookies.set("refresh_token", refresh_token)
    response: Response = await client.post(
        "api/auth/refresh",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.json().get("errors", [0])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_400_BAD_REQUEST
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")


@pytest.mark.asyncio()
async def test_refresh_user_access_token(
    client: AsyncClient,
    db_user: User,
) -> None:
    access_token: str = jwt_.generate_access_token(
        user_id=db_user.id,
        email=db_user.email,
    )

    client.cookies.set("refresh_token", access_token)
    response: Response = await client.post(
        "api/auth/refresh",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.json().get("errors", [0])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", 0) == status.HTTP_400_BAD_REQUEST
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")


@pytest.mark.asyncio()
async def test_refresh_user_no_authorization(
    client: AsyncClient,
    db_user: User,
) -> None:
    response: Response = await client.post(
        "api/auth/refresh",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", [0])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", db_user.id) == status.HTTP_401_UNAUTHORIZED
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")
