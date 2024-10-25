from typing import Any, TypeAlias

import jwt
import pytest

from app.core.auth import jwt
from app.core.config import settings
from app.core.database.models import User
from tests import testing_utils

_DecodedPayload: TypeAlias = jwt._TokenPayload | None


@pytest.mark.parametrize(
    "jwt_type",
    ["access", "refresh"],
)
def test_get_token_payload_access(
    jwt_type: jwt._TokenType,
    user_credentials: User,
    current_time: int,
) -> None:
    token: str = jwt.generate_token(
        jwt_type,
        user_id=user_credentials.id,
        email=user_credentials.email,
        current_time=current_time,
    )

    decoded_header: dict[str, Any] = jwt.get_unverified_header(token)
    decoded_payload: _DecodedPayload = jwt._get_token_payload(
        token,
        jwt_type,
    )

    assert decoded_header
    assert len(decoded_header) == len(["alg", "typ"])
    assert decoded_header.get("alg", -1) == settings.jwt.ALGORITHM
    assert decoded_header.get("typ", -1) == jwt_type
    assert decoded_payload
    assert len(decoded_payload) == len(["sub", "email", "exp", "iat"])
    assert decoded_payload.get("sub", -1) == str(user_credentials.id)
    assert decoded_payload.get("email", -1) == user_credentials.email
    assert decoded_payload.get("exp", -1) == testing_utils.get_token_exp(
        jwt_type,
        current_time,
    )
    assert decoded_payload["iat"] == current_time


@pytest.mark.parametrize(
    "token",
    [
        (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6I"
            "kpvaG4gRG9lIiwiZW1haWwiOiJqZG9lQG1haW"
            "wudGxkIn0.eyJleHAiOjE1MTYyMzkwMjJ9.7JvZ4"
        ),
        "",
    ],
)
def test_get_token_payload_invalid_token(token: str) -> None:
    payload: _DecodedPayload = jwt._get_token_payload(
        token,
        "access",
    )

    assert not payload


@pytest.mark.parametrize(
    ("jwt_type", "opposite_jwt_type"),
    [
        ("access", "refresh"),
        ("refresh", "access"),
    ],
)
def test_get_token_payload_invalid_type(
    jwt_type: jwt._TokenType,
    opposite_jwt_type: jwt._TokenType,
    user_credentials: User,
    current_time: int,
) -> None:
    token: str = jwt.generate_token(
        jwt_type,
        user_id=user_credentials.id,
        email=user_credentials.email,
        current_time=current_time,
    )

    payload: _DecodedPayload = jwt._get_token_payload(
        token,
        opposite_jwt_type,
    )

    assert not payload


@pytest.mark.parametrize(
    "jwt_type",
    ["access", "refresh"],
)
def test_get_token_payload_exired(
    jwt_type: jwt._TokenType,
    current_time: int,
    user_credentials: User,
) -> None:
    token: str = jwt.generate_token(
        jwt_type,
        user_id=user_credentials.id,
        email=user_credentials.email,
        current_time=2 * current_time
        - testing_utils.get_token_exp(jwt_type, current_time)
        - 1,
    )

    payload: _DecodedPayload = jwt._get_token_payload(
        token,
        jwt_type,
    )

    assert not payload


@pytest.mark.parametrize(
    "jwt_type",
    ["access", "refresh"],
)
def test_get_token_payload_invalid_signature(
    jwt_type: jwt._TokenType,
    current_time: int,
    user_credentials: User,
) -> None:
    key: str = "mG?!a.Ab=_C5aiQ1eS5Z{r,@(jDFyC." * 10

    payload: dict[str, Any] = {
        "sub": str(user_credentials.id),
        "email": user_credentials.email,
        "exp": current_time + 24 * 60 * 60,
        "iat": current_time - 24 * 60 * 60,
    }

    token: str = jwt.encode(
        payload,
        key,
        settings.jwt.ALGORITHM,
        headers={
            "typ": jwt_type,
        },
    )

    decoded_payload: _DecodedPayload = jwt._get_token_payload(
        token,
        "access",
    )

    assert not decoded_payload
