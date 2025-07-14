from typing import Annotated, Any

from fastapi import Cookie, Depends, HTTPException, status
from fastapi.security import APIKeyCookie
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database import database
from app.core.database.models import User
from app.core.settings import settings

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
    """Get the current user from the access token.

    This is a ` FastAPI ` dependency.

    Args:
        async_session: The async database session.
        access_token: The access token from the cookie.

    Returns:
        The current user.
    """
    if access_token is None:
        raise HTTPException(
            detail="Authentication required",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    token_payload: dict[str, Any] | None = get_token_payload(
        "access",
        token=access_token,
        key=settings.jwt.SECRET,
    )

    if token_payload is None:
        raise HTTPException(
            detail="Invalid token",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user: User | None = await crud.get_user_by_id(
        async_session=async_session,
        user_id=int(token_payload.get("sub", -1)),
    )

    if not user:
        raise HTTPException(
            detail="Invalid token",
            status_code=status.HTTP_400_BAD_REQUEST,
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
    """Get the current user from the refresh token.

    This is a ` FastAPI ` dependency.

    Args:
        async_session: The async database session.
        refresh_token: The refresh token from the cookie.

    Returns:
        The current user.
    """
    if refresh_token is None:
        raise HTTPException(
            detail="Authentication required",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    token_payload: dict[str, Any] | None = get_token_payload(
        "refresh",
        token=refresh_token,
        key=settings.jwt.SECRET,
    )

    if token_payload is None:
        raise HTTPException(
            detail="Invalid token",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user: User | None = await crud.get_user_by_id(
        async_session=async_session,
        user_id=int(token_payload.get("sub", -1)),
    )

    if not user:
        raise HTTPException(
            detail="Invalid token",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return user
