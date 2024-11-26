from typing import TypedDict

import jwt as pyjwt

from app.core.settings import settings

from .enums import Algorithm, TokenType


class _UserData(TypedDict):
    sub: str
    email: str


class TokenPayload(_UserData):
    exp: int
    iat: int


def _encode_token(
    token_type: TokenType,
    /,
    *,
    payload: _UserData,
    key: str,
    algorithm: Algorithm,
    current_time: int,
) -> str:
    expire: int = current_time
    if token_type == TokenType.ACCESS:
        expire += settings.jwt.JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES * 60
    else:
        expire += settings.jwt.JWT_REFRESH_TOKEN_EXPIRES_IN_DAYS * 24 * 60 * 60

    token_payload: TokenPayload = {
        "sub": payload["sub"],
        "email": payload["email"],
        "exp": expire,
        "iat": current_time,
    }

    return pyjwt.encode(
        payload=dict(token_payload),
        key=key,
        algorithm=algorithm.value,
        headers={
            "typ": token_type,
        },
        sort_headers=True,
    )


def generate_token(
    token_type: TokenType,
    /,
    *,
    user_id: int,
    email: str,
    current_time: int,
) -> str:
    """Generate a JWT token.

    Arguments:
        token_type (TokenType): The type of JWT token.
        user_id (int): The ` User ` id.
        email (str): The ` User ` email.
        current_time (int): The current time in seconds since the epoch.

    Returns:
        str: The encoded JWT token.
    """
    return _encode_token(
        token_type,
        payload={
            "sub": str(user_id),
            "email": email,
        },
        key=settings.jwt.JWT_SECRET,
        algorithm=settings.jwt.ALGORITHM,
        current_time=current_time,
    )


def get_token_payload(
    token_type: TokenType,
    /,
    *,
    token: str,
) -> TokenPayload | None:
    """Get payload from a JWT token.

    Arguments:
        token_type (TokenType): The type of JWT token.
        token (str): The JWT token.

    Returns:
        TokenPayload | None: The payload of the JWT token if the
                              token type matches and signature is valid,
                              otherwise None.

    """
    try:
        if (
            pyjwt.get_unverified_header(token).get("typ", None)
            != token_type.value
        ):
            return None

        token_payload: TokenPayload = pyjwt.decode(
            token,
            key=settings.jwt.JWT_SECRET,
            algorithms=[settings.jwt.ALGORITHM.value],
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
