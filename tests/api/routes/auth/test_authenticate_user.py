from typing import TYPE_CHECKING

import pytest
from fastapi import status
from httpx import AsyncClient, Response

from app.core.config import settings
from app.core.database.models import User
from tests import utils

if TYPE_CHECKING:
    from tests.api.types_ import Json


@pytest.mark.asyncio
async def test_authenticate_user(
    client: AsyncClient,
    db_user: User,
) -> None:
    json: Json = {
        "email": db_user.email,
        "password": utils.USER_PASSWORD,
    }

    response: Response = await client.post(
        "/api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_200_OK
    assert response.cookies.get("access_token", "")
    assert response.cookies.get("refresh_token", "")


@pytest.mark.asyncio
async def test_authenticate_user_incorrect_email(
    client: AsyncClient,
    db_user: User,
) -> None:
    json: Json = {
        "email": db_user.email + "a",
        "password": utils.USER_PASSWORD,
    }

    response: Response = await client.post(
        "/api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", [-1])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_401_UNAUTHORIZED
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")


@pytest.mark.asyncio
async def test_authenticate_user_incorrect_password(
    client: AsyncClient,
    db_user: User,
) -> None:
    json: Json = {
        "email": db_user.email,
        "password": utils.USER_PASSWORD[::-1],
    }

    response: Response = await client.post(
        "/api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", [-1])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_401_UNAUTHORIZED
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")


@pytest.mark.asyncio
async def test_authenticate_user_incorrect_all(
    client: AsyncClient,
    db_user: User,
) -> None:
    json: Json = {
        "email": db_user.email + "a",
        "password": utils.USER_PASSWORD[::-1],
    }

    response: Response = await client.post(
        "api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", [-1])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_401_UNAUTHORIZED
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")


@pytest.mark.asyncio
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
async def test_authenticate_user_invalid_email(
    email: str,
    client: AsyncClient,
) -> None:
    json: Json = {
        "email": email,
        "password": utils.USER_PASSWORD,
    }

    response: Response = await client.post(
        "/api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == 1
    assert utils.error_type_exists(response.json(), "email")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "password",
    [
        "",
        " " * (settings.data.PASSWORD_MAX_LENGTH + 1),
        "a" * (settings.data.PASSWORD_MIN_LENGTH - 1),
        "a" * (settings.data.PASSWORD_MAX_LENGTH + 1),
    ],
)
async def test_authenticate_user_invalid_password(
    password: str,
    client: AsyncClient,
) -> None:
    json: Json = {
        "email": utils.USER_EMAIL,
        "password": password,
    }

    response: Response = await client.post(
        "/api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == 1
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_authenticate_user_invalid_all(
    client: AsyncClient,
) -> None:
    json: Json = {
        "email": "a@b",
        "password": "a" * (settings.data.PASSWORD_MAX_LENGTH + 1),
    }

    response: Response = await client.post(
        "/api/auth/login",
        json=json,
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == len(["email", "password"])
    assert utils.error_type_exists(response.json(), "email")
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_authenticate_user_empty(
    client: AsyncClient,
) -> None:
    response: Response = await client.post(
        "/api/auth/login",
        json={},
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert len(response.json().get("errors", [])) == len(["email", "password"])
    assert utils.error_type_exists(response.json(), "email")
    assert utils.error_type_exists(response.json(), "password")
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_422_UNPROCESSABLE_ENTITY
