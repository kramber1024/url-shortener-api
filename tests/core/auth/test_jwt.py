from typing import Any, TypeAlias

import jwt as pyjwt
import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import HTTPError
from app.core.auth import jwt
from app.core.config import settings
from app.core.database.models import User
from tests import testing_utils

_DecodedHeader: TypeAlias = dict[str, Any]
_DecodedPayload: TypeAlias = jwt._TokenPayload | None


@pytest.mark.parametrize(
    "jwt_type",
    ["access", "refresh"],
)
def test__encode_token(
    jwt_type: jwt._TokenType,
    user_credentials: User,
    current_time: int,
) -> None:
    token: str = jwt._encode_token(
        jwt_type,
        payload={
            "sub": str(user_credentials.id),
            "email": user_credentials.email,
        },
        current_time=current_time,
    )

    decoded_header: _DecodedHeader = pyjwt.get_unverified_header(token)
    decoded_payload: Any = pyjwt.decode(
        token,
        key=settings.jwt.SECRET,
        algorithms=[settings.jwt.ALGORITHM],
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
        current_time=current_time,
    )
    assert decoded_payload["iat"] == current_time


@pytest.mark.parametrize(
    "jwt_type",
    ["access", "refresh"],
)
def test_generate_token(
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

    decoded_header: _DecodedHeader = pyjwt.get_unverified_header(token)
    decoded_payload: Any = pyjwt.decode(
        token,
        key=settings.jwt.SECRET,
        algorithms=[settings.jwt.ALGORITHM],
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
        current_time=current_time,
    )
    assert decoded_payload["iat"] == current_time


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

    decoded_header: _DecodedHeader = pyjwt.get_unverified_header(token)
    decoded_payload: _DecodedPayload = jwt._get_token_payload(
        jwt_type,
        token=token,
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
        current_time=current_time,
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
        "access",
        token=token,
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
        opposite_jwt_type,
        token=token,
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
        - testing_utils.get_token_exp(jwt_type, current_time=current_time)
        - 1,
    )

    payload: _DecodedPayload = jwt._get_token_payload(
        jwt_type,
        token=token,
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

    token: str = pyjwt.encode(
        payload,
        key,
        settings.jwt.ALGORITHM,
        headers={
            "typ": jwt_type,
        },
    )

    decoded_payload: _DecodedPayload = jwt._get_token_payload(
        "access",
        token=token,
    )

    assert not decoded_payload


@pytest.mark.asyncio
async def test_current_user(
    session: AsyncSession,
    access_token: str,
) -> None:
    current_user: User = await jwt.current_user(
        session=session,
        access_token=access_token,
    )

    assert current_user
    assert current_user.first_name == testing_utils.USER_FIRST_NAME
    assert current_user.last_name == testing_utils.USER_LAST_NAME


@pytest.mark.asyncio
async def test_current_user_none_token(
    session: AsyncSession,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt.current_user(
            session=session,
            access_token=None,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_current_user_no_user(
    session: AsyncSession,
    current_time: int,
) -> None:
    token: str = jwt.generate_token(
        "access",
        user_id=-1,
        email="",
        current_time=current_time,
    )

    with pytest.raises(HTTPError) as exc:
        await jwt.current_user(
            session=session,
            access_token=token,
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_current_user_invalid_token(
    session: AsyncSession,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt.current_user(
            session=session,
            access_token=(
                f"{"c114:a6f1:2cb2:f14d:3384:4e71:753f:ebb1" * 10}."
                f"{"email@example.com" * 20}."
                f"{"0" * 100}"
            ),
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_refreshed_user(
    session: AsyncSession,
    refresh_token: str,
) -> None:
    refreshed_user: User = await jwt.refreshed_user(
        session=session,
        refresh_token=refresh_token,
    )

    assert refreshed_user
    assert refreshed_user.id in testing_utils.SNOWFLAKE_RANGE
    assert refreshed_user.first_name == testing_utils.USER_FIRST_NAME
    assert refreshed_user.last_name == testing_utils.USER_LAST_NAME
    assert refreshed_user.email == testing_utils.format_email(
        testing_utils.USER_EMAIL,
    )
    assert not refreshed_user.phone
    assert refreshed_user.password != testing_utils.USER_PASSWORD
    assert refreshed_user.is_password_valid(testing_utils.USER_PASSWORD)
    assert refreshed_user.status
    assert refreshed_user.status.user_id == refreshed_user.id
    assert not refreshed_user.status.email_verified
    assert not refreshed_user.status.phone_verified
    assert refreshed_user.status.active
    assert not refreshed_user.status.premium
    assert not refreshed_user.urls


@pytest.mark.asyncio
async def test_refreshed_user_none_token(
    session: AsyncSession,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt.refreshed_user(
            session=session,
            refresh_token=None,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_refreshed_user_no_token(
    session: AsyncSession,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt.refreshed_user(
            session=session,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_refreshed_user_no_user(
    session: AsyncSession,
    current_time: int,
) -> None:
    id_: int = 5187728381231
    email: str = "Ettie94@gmail.com"

    token: str = jwt.generate_token(
        "refresh",
        user_id=id_,
        email=email,
        current_time=current_time,
    )

    with pytest.raises(HTTPError) as exc:
        await jwt.refreshed_user(
            session=session,
            refresh_token=token,
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_refreshed_user_invalid_token(
    session: AsyncSession,
    user_credentials: User,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt.refreshed_user(
            session=session,
            refresh_token=(
                f"{user_credentials.email * 2}."
                f"{user_credentials.first_name * 2}."
                f"{user_credentials.password * 2}"
            ),
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_400_BAD_REQUEST
