from typing import TypeAlias

import pytest
from fastapi import status
from httpx import AsyncClient, Response

from app.core.auth import jwt_
from app.core.database.models import User

_Tokens: TypeAlias = tuple[str, str]


@pytest.fixture
def tokens(db_user: User, current_time: int) -> _Tokens:
    """Fixture for generating access and refresh tokens.

    Get access and refresh tokens using functions/methods from ` core.auth.jwt_ ` module

    Returns
    -------
        _Tokens: Tuple of access and refresh tokens.

    """
    # Subtract 10 seconds from the current time to prevent token collision.
    access_token: str = jwt_.generate_token(
        "access",
        user_id=db_user.id,
        email=db_user.email,
        current_time=current_time - 10,
    )

    refresh_token: str = jwt_.generate_token(
        "refresh",
        user_id=db_user.id,
        email=db_user.email,
        current_time=current_time - 10,
    )

    return access_token, refresh_token


@pytest.mark.asyncio()
async def test_refresh_user(
    client: AsyncClient,
    tokens: _Tokens,
) -> None:
    client.cookies.set("access_token", tokens[0])
    client.cookies.set("refresh_token", tokens[1])
    response: Response = await client.post(
        "/api/auth/refresh",
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_200_OK
    assert response.cookies.get("access_token", "")
    assert response.cookies.get("refresh_token", "")
    assert response.cookies.get("access_token") != tokens[0]
    assert response.cookies.get("refresh_token") != tokens[1]


@pytest.mark.asyncio()
async def test_refresh_user_invalid_token(
    client: AsyncClient,
) -> None:
    refresh_token: str = (
        "wnce8OakjfsPgNSWvlZosGgSWkXPhR."
        "19Q5n3vX04pJorG6Ps2LYzrmZr1Xdc."
        "fO43J2Amatx31wE9iLUDFcxm08KPva"
    )

    client.cookies.set("refresh_token", refresh_token)
    response: Response = await client.post(
        "/api/auth/refresh",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.json().get("errors", [-1])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_400_BAD_REQUEST
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")


@pytest.mark.asyncio()
async def test_refresh_user_access_token(
    client: AsyncClient,
    tokens: _Tokens,
) -> None:
    client.cookies.set("refresh_token", tokens[0])
    response: Response = await client.post(
        "/api/auth/refresh",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(response.json().get("errors", [-1])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_400_BAD_REQUEST
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")


@pytest.mark.asyncio()
async def test_refresh_user_no_authorization(
    client: AsyncClient,
) -> None:
    response: Response = await client.post(
        "/api/auth/refresh",
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response.json().get("errors", [-1])) == 0
    assert response.json().get("message", "")
    assert response.json().get("status", -1) == status.HTTP_401_UNAUTHORIZED
    assert not response.cookies.get("access_token", "")
    assert not response.cookies.get("refresh_token", "")
