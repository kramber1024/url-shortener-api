from typing import Any, Literal, TypedDict

import jwt as pyjwt

from app.core.settings import settings


class _UserData(TypedDict):
    sub: str
    email: str


class _TokenPayload(_UserData):
    exp: int
    iat: int


def _encode_token(
    token_type: Literal["access", "refresh"],
    /,
    *,
    payload: _UserData,
    key: str,
    algorithm: str,
    current_time: int,
) -> str:
    expire: int = current_time
    if (token_type,) == ("access",):
        expire += settings.jwt.ACCESS_TOKEN_EXPIRES_IN_MINUTES * 60
    else:
        expire += settings.jwt.REFRESH_TOKEN_EXPIRES_IN_DAYS * 24 * 60 * 60

    token_payload: _TokenPayload = {
        "sub": payload["sub"],
        "email": payload["email"],
        "exp": expire,
        "iat": current_time,
    }

    return pyjwt.encode(
        payload=dict(token_payload),
        key=key,
        algorithm=algorithm,
        headers={
            "typ": token_type,
        },
        sort_headers=True,
    )


def generate_token(
    token_type: Literal["access", "refresh"],
    /,
    *,
    user_id: int,
    email: str,
    key: str,
    current_time: int,
) -> str:
    """Generate a JWT token.

    Arguments:
        token_type: The type of JWT token.
        user_id: The ` User ` id.
        email: The ` User ` email.
        key: The key to encode the JWT token with.
        current_time: The current time in seconds.

    Returns:
        The encoded JWT token.
    """
    return _encode_token(
        token_type,
        payload={
            "sub": str(user_id),
            "email": email,
        },
        key=key,
        algorithm=settings.jwt.ALGORITHM,
        current_time=current_time,
    )


def get_token_payload(
    token_type: Literal["access", "refresh"],
    /,
    *,
    token: str,
    key: str,
) -> dict[str, Any] | None:
    """Get payload from a JWT token.

    Arguments:
        token_type: The type of JWT token.
        token: The JWT token.
        key: The key to decode the JWT token with.

    Returns:
        The payload of the JWT token if the token type matches and signature
            is valid, otherwise ` None `.
    """
    try:
        if pyjwt.get_unverified_header(token).get("typ", None) != token_type:
            return None

        token_payload: dict[str, Any] = pyjwt.decode(
            token,
            key=key,
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

    except pyjwt.InvalidTokenError:
        return None

    return token_payload
