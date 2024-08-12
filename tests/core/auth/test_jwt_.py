import datetime

import jwt
import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import HTTPError
from app.core.auth import jwt_
from app.core.config import settings
from app.core.database.models import User
from tests import utils


def test__encode_jwt_access(
    db_user: User,
) -> None:
    payload: dict[str, str | int] = {
        "sub": str(db_user.id),
        "email": db_user.email,
    }

    token: str = jwt_._encode_jwt(
        jwt_type="access",
        payload=payload,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] = jwt.decode(
        token,
        key=settings.jwt.SECRET,
        algorithms=[settings.jwt.ALGORITHM],
    )

    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "access"
    assert "sub" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == str(db_user.id)
    assert decoded_payload["email"] == db_user.email
    assert decoded_payload["exp"] in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"]) + settings.jwt.ACCESS_TOKEN_EXPIRES_MINUTES * 61,
    )
    assert decoded_payload["iat"] in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp()) + 61,
    )


def test__encode_jwt_refresh(
    db_user: User,
) -> None:
    payload: dict[str, str | int] = {
        "sub": str(db_user.id),
        "email": db_user.email,
    }

    token: str = jwt_._encode_jwt(
        jwt_type="refresh",
        payload=payload,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] = jwt.decode(
        token,
        key=settings.jwt.SECRET,
        algorithms=[settings.jwt.ALGORITHM],
    )

    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "refresh"
    assert "sub" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == str(db_user.id)
    assert decoded_payload["email"] == db_user.email
    assert decoded_payload["exp"] in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"])
        + settings.jwt.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 61,
    )
    assert decoded_payload["iat"] in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp()) + 61,
    )


def test_generate_access_token(
    db_user: User,
) -> None:
    token: str = jwt_.generate_access_token(
        user_id=db_user.id,
        email=db_user.email,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] = jwt.decode(
        token,
        key=settings.jwt.SECRET,
        algorithms=[settings.jwt.ALGORITHM],
    )

    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "access"
    assert "sub" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == str(db_user.id)
    assert decoded_payload["email"] == db_user.email
    assert decoded_payload["exp"] in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"]) + settings.jwt.ACCESS_TOKEN_EXPIRES_MINUTES * 61,
    )
    assert decoded_payload["iat"] in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp()) + 61,
    )


def test_generate_refresh_token(
    db_user: User,
) -> None:
    token: str = jwt_.generate_refresh_token(
        user_id=db_user.id,
        email=db_user.email,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] = jwt.decode(
        token,
        key=settings.jwt.SECRET,
        algorithms=[settings.jwt.ALGORITHM],
    )

    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "refresh"
    assert "sub" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == str(db_user.id)
    assert decoded_payload["email"] == db_user.email
    assert decoded_payload["exp"] in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"])
        + settings.jwt.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 61,
    )
    assert decoded_payload["iat"] in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp()) + 60,
    )


def test_get_token_payload_access(
    db_user: User,
) -> None:
    token: str = jwt_.generate_access_token(
        user_id=db_user.id,
        email=db_user.email,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] | None = jwt_.get_token_payload(
        token=token,
        jwt_type="access",
    )

    assert decoded_payload
    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "access"
    assert "sub" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == str(db_user.id)
    assert decoded_payload["email"] == db_user.email
    assert int(decoded_payload["exp"]) in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"]) + settings.jwt.ACCESS_TOKEN_EXPIRES_MINUTES * 61,
    )
    assert int(decoded_payload["iat"]) in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp()) + 61,
    )


def test_get_token_payload_refresh(
    db_user: User,
) -> None:
    token: str = jwt_.generate_refresh_token(
        user_id=db_user.id,
        email=db_user.email,
    )

    decoded_headers: dict[str, str] = jwt.get_unverified_header(token)
    decoded_payload: dict[str, str | int] | None = jwt_.get_token_payload(
        token=token,
        jwt_type="refresh",
    )

    assert decoded_payload
    assert "alg" in decoded_headers
    assert "typ" in decoded_headers
    assert decoded_headers["alg"] == settings.jwt.ALGORITHM
    assert decoded_headers["typ"] == "refresh"
    assert "sub" in decoded_payload
    assert "email" in decoded_payload
    assert "exp" in decoded_payload
    assert "iat" in decoded_payload
    assert decoded_payload["sub"] == str(db_user.id)
    assert decoded_payload["email"] == db_user.email
    assert decoded_payload["exp"] in range(
        int(decoded_payload["iat"]),
        int(decoded_payload["iat"])
        + settings.jwt.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 61,
    )
    assert decoded_payload["iat"] in range(
        int(datetime.datetime.now(datetime.UTC).timestamp()),
        int(datetime.datetime.now(datetime.UTC).timestamp()) + 60,
    )


def test_get_token_payload_invalid_token() -> None:
    token: str = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
        "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiZW1haWwiOiJqZG9lQG1haWwudGxkIn0."
        "eyJleHAiOjE1MTYyMzkwMjJ9.7JvZ4"
    )

    payload: dict[str, str | int] | None = jwt_.get_token_payload(
        token=token,
        jwt_type="access",
    )

    assert payload is None


def test_get_token_payload_invalid_type(
    db_user: User,
) -> None:
    token: str = jwt_.generate_refresh_token(
        user_id=db_user.id,
        email=db_user.email,
    )

    payload: dict[str, str | int] | None = jwt_.get_token_payload(
        token=token,
        jwt_type="access",
    )

    assert payload is None


def test_get_token_payload_invalid_signature() -> None:
    key: str = "mG?!a.Ab=_C5aiQ1eS5Z{r,@(jDFyC" * 10
    now: int = int(datetime.datetime.now(datetime.UTC).timestamp())

    payload: dict[str, str | int] = {
        "sub": 1234561231227890,
        "name": "Lorenzo Swift",
        "email": "Garnet.Herman83@yahoo.com",
        "exp": now + 24 * 60 * 60,
        "iat": now - 24 * 60 * 60,
    }

    token: str = jwt.encode(
        payload,
        key,
        settings.jwt.ALGORITHM,
        headers={
            "typ": "access",
        },
    )

    decoded_payload: dict[str, str | int] | None = jwt_.get_token_payload(
        token=token,
        jwt_type="access",
    )

    assert decoded_payload is None


@pytest.mark.asyncio
async def test_get_current_user(
    session: AsyncSession,
    db_user: User,
) -> None:
    token: str = jwt_.generate_access_token(
        user_id=db_user.id,
        email=db_user.email,
    )

    current_user: User = await jwt_.get_current_user(
        session=session,
        access_token=token,
    )

    assert current_user.id in utils.SNOWFLAKE_RANGE
    assert current_user.first_name == db_user.first_name
    assert current_user.last_name == db_user.last_name
    assert current_user.email == db_user.email
    assert current_user.phone is None
    assert current_user.password == db_user.password
    assert current_user.is_password_valid(utils.USER_PASSWORD)


@pytest.mark.asyncio
async def test_get_current_user_none_token(
    session: AsyncSession,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt_.get_current_user(
            session=session,
            access_token=None,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_current_user_no_user(
    session: AsyncSession,
) -> None:
    id_: int = 1234567890123498
    email: str = "Christina.Kuvalis@yahoo.com"

    token: str = jwt_.generate_access_token(
        user_id=id_,
        email=email,
    )

    with pytest.raises(HTTPError) as exc:
        await jwt_.get_current_user(
            session=session,
            access_token=token,
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(
    session: AsyncSession,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt_.get_current_user(
            session=session,
            access_token=(
                f"{"c114:a6f1:2cb2:f14d:3384:4e71:753f:ebb1" * 10}."
                f"{"Nestor.Lind43@yahoo.com" * 20}."
                f"{"1" * 100}"
            ),
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_refreshed_user(
    session: AsyncSession,
    db_user: User,
) -> None:
    token: str = jwt_.generate_refresh_token(
        user_id=db_user.id,
        email=db_user.email,
    )

    refreshed_user: User = await jwt_.get_refreshed_user(
        session=session,
        refresh_token=token,
    )

    assert refreshed_user.id in utils.SNOWFLAKE_RANGE
    assert refreshed_user.first_name == db_user.first_name
    assert refreshed_user.last_name == db_user.last_name
    assert refreshed_user.email == db_user.email
    assert refreshed_user.phone is None
    assert refreshed_user.password == db_user.password
    assert refreshed_user.is_password_valid(utils.USER_PASSWORD)


@pytest.mark.asyncio
async def test_get_refreshed_user_none_token(
    session: AsyncSession,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt_.get_refreshed_user(
            session=session,
            refresh_token=None,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_refreshed_user_no_token(
    session: AsyncSession,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt_.get_refreshed_user(
            session=session,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_refreshed_user_no_user(
    session: AsyncSession,
) -> None:
    id_: int = 5187728381231
    email: str = "Ettie94@gmail.com"

    token: str = jwt_.generate_refresh_token(
        user_id=id_,
        email=email,
    )

    with pytest.raises(HTTPError) as exc:
        await jwt_.get_refreshed_user(
            session=session,
            refresh_token=token,
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_refreshed_user_invalid_token(
    session: AsyncSession,
    db_user: User,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt_.get_refreshed_user(
            session=session,
            refresh_token=(
                f"{db_user.email * 2}."
                f"{db_user.first_name * 2}."
                f"{db_user.password * 2}"
            ),
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_400_BAD_REQUEST
