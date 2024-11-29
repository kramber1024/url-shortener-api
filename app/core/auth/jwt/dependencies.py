from typing import Annotated, Any

from fastapi import Cookie, Depends, status
from fastapi.security import APIKeyCookie
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.exceptions import HTTPError
from app.core.database import database
from app.core.database.models import User
from app.core.settings import settings

from .enums import TokenType
from .jwt import get_token_payload

api_key_cookie: APIKeyCookie = APIKeyCookie(
    name="access_token",
    description="Access token",
    auto_error=False,
)


async def get_current_user(
    async_session: Annotated[
        AsyncSession,
        Depends(database.get_async_session),
    ],
    access_token: Annotated[
        str | None,
        Depends(api_key_cookie),
    ],
) -> User:
    if access_token is None:
        raise HTTPError(
            errors=[],
            message="Authorization required",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token_payload: dict[str, Any] | None = get_token_payload(
        TokenType.ACCESS,
        token=access_token,
        key=settings.jwt.JWT_SECRET,
    )

    if token_payload is None:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=status.HTTP_400_BAD_REQUEST,
        )

    user: User | None = await crud.get_user_by_id(
        async_session=async_session,
        user_id=int(token_payload.get("sub", -1)),
    )

    if not user:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=status.HTTP_400_BAD_REQUEST,
        )

    return user


async def get_refreshed_user(
    async_session: Annotated[
        AsyncSession,
        Depends(database.get_async_session),
    ],
    refresh_token: Annotated[
        str | None,
        Cookie(
            description="Refresh token",
        ),
    ] = None,
) -> User:
    if refresh_token is None:
        raise HTTPError(
            errors=[],
            message="Authorization required",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    token_payload: dict[str, Any] | None = get_token_payload(
        TokenType.REFRESH,
        token=refresh_token,
        key=settings.jwt.JWT_SECRET,
    )

    if token_payload is None:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=status.HTTP_400_BAD_REQUEST,
        )

    user: User | None = await crud.get_user_by_id(
        async_session=async_session,
        user_id=int(token_payload.get("sub", -1)),
    )

    if not user:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=status.HTTP_400_BAD_REQUEST,
        )

    return user
