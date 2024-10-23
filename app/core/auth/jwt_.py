from typing import Annotated, Literal, TypeAlias, TypedDict

import jwt
from fastapi import Cookie, Depends, status
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
    jwt_type: _TokenType,
    /,
    *,
    payload: _UserData,
    key: str = settings.jwt.SECRET,
    algorithm: JWTAlgorithm = settings.jwt.ALGORITHM,
    current_time: int,
) -> str:
    """Generate a JWT token.

    Args:
    ----
        jwt_type (_TokenType): The type of JWT token.
                               Either "access" or "refresh".
        payload (_UserData): The payload of the JWT token.
        current_time (int): The current time in seconds since the epoch.
        key (str, optional): Secret key to sign the token
                             Defaults to settings.jwt.SECRET.
        algorithm (JWTAlgorithm, optional): The algorithm to use for
                                            signing the token.
                                            Defaults to settings.jwt.ALGORITHM.

    Returns:
    -------
        The JWT token.

    """
    if jwt_type == "access":
        expire: int = (
            current_time + settings.jwt.ACCESS_TOKEN_EXPIRES_MINUTES * 60
        )
    else:
        expire = (
            current_time
            + settings.jwt.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 60
        )

    token_payload: _TokenPayload = {
        "sub": payload.get("sub", ""),
        "email": payload.get("email", ""),
        "exp": expire,
        "iat": current_time,
    }

    return jwt.encode(
        payload=dict(token_payload),
        key=key,
        algorithm=algorithm,
        headers={
            "typ": jwt_type,
        },
    )


def generate_token(
    jwt_type: _TokenType,
    /,
    *,
    user_id: int,
    email: str,
    current_time: int,
) -> str:
    """Generate a JWT token.

    Args:
    ----
        jwt_type (_TokenType): The type of JWT token.
                               Either "access" or "refresh".
        user_id (int): The ` User ` id.
        email (str): The ` User ` email.
        current_time (int): The current time in seconds since the epoch.

    Returns:
    -------
        The encoded JWT token.

    Example:
    -------
    >>> jwt_type = "access"
    >>> user_id = 1234567890
    >>> email = "email@example.com"
    >>> current_time = 1719956372
    >>> generate_token(
    ...     jwt_type,
    ...     user_id,
    ...     email,
    ...     current_time,
    ... )
    ... (
    ...     "eyJhbGciOiJIUzI1NiIsInR5cCI6ImFjY2VzcyJ9.eyJzdWIiOiIxMjM0N"
    ...     "TY3ODkwIiwiZW1haWwiOiJlbWFpbEBleGFtcGxlLmNvbSIsImV4cCI6MTcx"
    ...     "OTk1OTk3MiwiaWF0IjoxNzE5OTU2MzcyfQ.AXEWuud-NgdLFsEV8NQ93moZZ"
    ...     "asu2zUZJF3oCIo2lBE"
    ... )

    """
    return _encode_token(
        jwt_type,
        payload={
            "sub": str(user_id),
            "email": email,
        },
        current_time=current_time,
    )


def _get_token_payload(
    jwt_type: _TokenType,
    /,
    *,
    token: str,
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
                              token type matches and signature is valid,
                              otherwise None.

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
            status=status.HTTP_401_UNAUTHORIZED,
        )

    payload: _TokenPayload | None = _get_token_payload(
        "access",
        token=access_token,
    )

    if payload is None:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=status.HTTP_400_BAD_REQUEST,
        )

    user: User | None = await crud.get_user_by_id(
        session=session,
        id_=int(payload.get("sub", -1)),
    )

    if user is None:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=status.HTTP_400_BAD_REQUEST,
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
            status=status.HTTP_401_UNAUTHORIZED,
        )

    payload: _TokenPayload | None = _get_token_payload(
        "refresh",
        token=refresh_token,
    )

    if payload is None:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=status.HTTP_400_BAD_REQUEST,
        )

    user: User | None = await crud.get_user_by_id(
        session=session,
        id_=int(payload.get("sub", -1)),
    )

    if user is None:
        raise HTTPError(
            errors=[],
            message="Invalid token",
            status=status.HTTP_400_BAD_REQUEST,
        )

    return user
