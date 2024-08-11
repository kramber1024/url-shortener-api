import datetime
from typing import Annotated, Literal

import jwt
from fastapi import Cookie, Depends
from fastapi.security import APIKeyCookie
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.exceptions import HTTPError
from app.core.config import settings
from app.core.database import db
from app.core.database.models import User

access_cookie_scheme: APIKeyCookie = APIKeyCookie(
    name="access_token",
    auto_error=False,
)


def _encode_jwt(
    jwt_type: Literal["access", "refresh"],
    payload: dict[str, str | int],
    key: str = settings.jwt.SECRET,
    algorithm: str = settings.jwt.ALGORITHM,
) -> str:
    now: int = int(datetime.datetime.now(datetime.UTC).timestamp())

    if jwt_type == "access":
        expire: int = now + settings.jwt.ACCESS_TOKEN_EXPIRES_MINUTES * 60
    else:
        expire = now + settings.jwt.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 60

    payload.update(
        {
            "exp": expire,
            "iat": now,
        },
    )
    return jwt.encode(
        payload,
        key,
        algorithm,
        headers={
            "typ": jwt_type,
        },
    )


def generate_access_token(
    user_id: int,
    email: str,
) -> str:
    return _encode_jwt(
        jwt_type="access",
        payload={
            "sub": str(user_id),
            "email": email,
        },
    )


def generate_refresh_token(
    user_id: int,
    email: str,
) -> str:
    return _encode_jwt(
        jwt_type="refresh",
        payload={
            "sub": str(user_id),
            "email": email,
        },
    )


def get_token_payload(
    token: str,
    jwt_type: Literal["access", "refresh"],
) -> dict[str, str | int] | None:
    """Get payload from a JWT token.

    Args:
    ----
        token: The JWT token.
        jwt_type: The type of JWT token. Either "access" or "refresh".

    Returns:
    -------
        dict[str, str | int] | None: The payload of the JWT token if the
        token type matches and signature is valid, otherwise None.

    Raises:
    ------
        None

    Example:
    -------
        >>> token = "eyJhbGciOiJIUzI1NiIsInR5cCI6ImFjY2VzcyJ9.eyJzdWIiOiIxM\
            jM0NTY3ODkwIiwiZW1haWwiOiJleGFtcGxlQGVtYWlsLnRsZCIsImV4cCI6MTcx\
            OTk1OTk3MiwiaWF0IjoxNzE5OTU2MzcyfQ.SU7oI8z5-MVI4GpiOdMtv1eVB-J2bMovCyyfXsHw-Vo"
        >>> jwt_type = "access"
        >>> get_token_payload(token, jwt_type)
        {"sub": "1234567890", "email": "example@email.tld",
        "exp": 1719959972, "iat": 1719956372}

    """
    try:
        if jwt.get_unverified_header(token).get("typ", "") != jwt_type:
            return None

        token_payload: dict[str, str | int] = jwt.decode(
            token,
            settings.jwt.SECRET,
            algorithms=[settings.jwt.ALGORITHM],
            options={
                "require": [
                    "sub",
                    "email",
                    "exp",
                    "iat",
                ],
                "verify_exp": True,
                "verify_signature": True,
            },
        )

    except jwt.InvalidTokenError:
        return None

    return token_payload


async def get_current_user(
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
    ],
    access_token: Annotated[
        str | None,
        Depends(access_cookie_scheme),
    ],
) -> User:
    if access_token is None:
        raise HTTPError(
            errors=[],
            message="Authorization required",
            status=401,
        )

    payload: dict[str, str | int] | None = get_token_payload(
        access_token,
        jwt_type="access",
    )

    if payload is None:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=400,
        )

    user: User | None = await crud.get_user_by_id(
        session=session,
        id_=int(payload.get("sub", -1)),
    )

    if user is None:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=400,
        )

    return user


async def get_refreshed_user(
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
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
            status=401,
        )

    payload: dict[str, str | int] | None = get_token_payload(
        refresh_token,
        jwt_type="refresh",
    )

    if payload is None:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=400,
        )

    user: User | None = await crud.get_user_by_id(
        session=session,
        id_=int(payload.get("sub", -1)),
    )

    if user is None:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=400,
        )

    return user
