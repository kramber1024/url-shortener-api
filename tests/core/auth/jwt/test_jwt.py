from typing import Any, Literal

import jwt as pyjwt
import pytest

from app.core.auth.jwt import generate_token, get_token_payload
from app.core.settings import settings


@pytest.fixture(scope="package")
def key() -> str:
    return "key"


@pytest.fixture(scope="package")
def user_id() -> int:
    return 1


@pytest.fixture(scope="package")
def email() -> str:
    return "john.doe@example.com"


@pytest.mark.parametrize("token_type", ["access", "refresh"])
def test_generate_token(
    token_type: Literal["access", "refresh"],
    user_id: int,
    email: str,
    key: str,
    current_time: int,
) -> None:
    token: str = generate_token(
        token_type,
        user_id=user_id,
        email=email,
        key=key,
        current_time=current_time,
    )

    token_payload = pyjwt.decode(
        token,
        key=key,
        algorithms=[settings.jwt.ALGORITHM],
    )

    assert isinstance(token, str)
    assert len(token) > 0
    assert pyjwt.get_unverified_header(token).get("typ", None) == token_type
    assert token_payload.get("sub") == str(user_id)
    assert token_payload.get("email") == email


@pytest.mark.parametrize("token_type", ["access", "refresh"])
def test_get_token_payload(
    token_type: Literal["access", "refresh"],
    user_id: int,
    email: str,
    key: str,
    current_time: int,
) -> None:
    token: str = generate_token(
        token_type,
        user_id=user_id,
        email=email,
        key=key,
        current_time=current_time,
    )

    token_payload: dict[str, Any] | None = get_token_payload(
        token_type,
        token=token,
        key=key,
    )

    assert token_payload is not None
    assert token_payload.get("sub") == str(user_id)
    assert token_payload.get("email") == "john.doe@example.com"
    assert token_payload.get("exp")
    assert token_payload.get("iat")


@pytest.mark.parametrize(
    ("token_type", "invalid_token_type"),
    [
        ("access", "refresh"),
        ("refresh", "access"),
    ],
)
def test_get_token_payload_invalid_token_type(
    token_type: Literal["access", "refresh"],
    invalid_token_type: Literal["access", "refresh"],
    key: str,
    current_time: int,
) -> None:
    token: str = generate_token(
        token_type,
        user_id=1,
        email="john.doe@example.com",
        key=key,
        current_time=current_time,
    )

    token_payload: dict[str, Any] | None = get_token_payload(
        invalid_token_type,
        token=token,
        key=key,
    )

    assert token_payload is None


def test_get_token_payload_invalid_key(
    key: str,
    user_id: int,
    email: str,
    current_time: int,
) -> None:
    token: str = generate_token(
        "access",
        user_id=user_id,
        email=email,
        key=key + "invalid",
        current_time=current_time,
    )

    token_payload: dict[str, Any] | None = get_token_payload(
        "access",
        token=token,
        key=key,
    )

    assert token_payload is None
