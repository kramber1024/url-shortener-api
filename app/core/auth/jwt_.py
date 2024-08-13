import datetime
from typing import Annotated, Literal, TypeAlias, TypedDict

import jwt
from fastapi import Cookie, Depends
from fastapi.security import APIKeyCookie
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.exceptions import HTTPError
from app.core.config import JWTAlgorithm, settings
from app.core.database import db
from app.core.database.models import User

_TokenType: TypeAlias = Literal["access", "refresh"]

access_cookie_scheme: APIKeyCookie = APIKeyCookie(
    name="access_token",
    auto_error=False,
)


class _UserData(TypedDict):
    sub: str
    email: str


class _TokenPayload(TypedDict, _UserData):
    exp: int
    iat: int


def _encode_token(
    type_: _TokenType,
    payload: _UserData,
    key: str = settings.jwt.SECRET,
    algorithm: JWTAlgorithm = settings.jwt.ALGORITHM,
) -> str:
    now: int = int(datetime.datetime.now(datetime.UTC).timestamp())

    if type_ == "access":
        expire: int = now + settings.jwt.ACCESS_TOKEN_EXPIRES_MINUTES * 60
    else:
        expire = now + settings.jwt.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 60

    token_payload: _TokenPayload = {
        "sub": payload.get("sub", ""),
        "email": payload.get("email", ""),
        "exp": expire,
        "iat": now,
    }

    return jwt.encode(
        dict(token_payload),
        key,
        algorithm,
        headers={
            "typ": type_,
        },
    )


def generate_access_token(
    user_id: int,
    email: str,
) -> str:
    return _encode_token(
        type_="access",
        payload={
            "sub": str(user_id),
            "email": email,
        },
    )


def generate_refresh_token(
    user_id: int,
    email: str,
) -> str:
    return _encode_token(
        type_="refresh",
        payload={
            "sub": str(user_id),
            "email": email,
        },
    )


def get_token_payload(
    token: str,
    jwt_type: _TokenType,
) -> _TokenPayload | None:
    """Get payload from a JWT token.

    Args:
    ----
        token (str): The JWT token.
        jwt_type ("access" | "refresh"): The type of JWT token.
        Either "access" or "refresh".

    Returns:
    -------
        _TokenPayload | None: The payload of the JWT token if the
        token type matches and signature is valid, otherwise None.

    Example:
    -------
    >>> token = "eyJhbGciOiJIUzI1NiIsInR5cCI6ImFjY2VzcyJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwiZ\
    W1haWwiOiJleGFtcGxlQGVtYWlsLnRsZCIsImV4cCI6MTcxOTk1OTk3MiwiaWF0IjoxNzE5OTU2Mzcy\
    fQ.SU7oI8z5-MVI4GpiOdMtv1eVB-J2bMovCyyfXsHw-Vo"
    >>> jwt_type = "access"
    >>> get_token_payload(token, jwt_type)
    {"sub": "1234567890", "email": "example@email.tld",
    "exp": 1719959972, "iat": 1719956372}

    """
    try:
        if jwt.get_unverified_header(token).get("typ", "") != jwt_type:
            return None

        token_payload: _TokenPayload = jwt.decode(
            token,
            key=settings.jwt.SECRET,
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

    payload: _TokenPayload | None = get_token_payload(
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

    payload: _TokenPayload | None = get_token_payload(
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
