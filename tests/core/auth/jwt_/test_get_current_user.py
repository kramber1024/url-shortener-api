import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import HTTPError
from app.core.auth import jwt_
from app.core.database.models import User
from tests import utils


@pytest.fixture
def access_token(db_user: User, current_time: int) -> str:
    return jwt_.generate_token(
        "access",
        user_id=db_user.id,
        email=db_user.email,
        current_time=current_time,
    )


@pytest.mark.asyncio
async def test_get_current_user(
    session: AsyncSession,
    access_token: str,
) -> None:
    current_user: User = await jwt_.get_current_user(
        session=session,
        access_token=access_token,
    )

    assert current_user
    assert current_user.id in utils.SNOWFLAKE_RANGE
    assert current_user.first_name == utils.USER_FIRST_NAME
    assert current_user.last_name == utils.USER_LAST_NAME
    assert current_user.email == utils.format_email(utils.USER_EMAIL)
    assert not current_user.phone
    assert current_user.password != utils.USER_PASSWORD
    assert current_user.is_password_valid(utils.USER_PASSWORD)
    assert current_user.status
    assert current_user.status.user_id == current_user.id
    assert not current_user.status.email_verified
    assert not current_user.status.phone_verified
    assert current_user.status.active
    assert not current_user.status.premium
    assert not current_user.urls


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
    current_time: int,
) -> None:
    token: str = jwt_.generate_token(
        "access",
        user_id=-1,
        email="",
        current_time=current_time,
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
                f"{"email@example.com" * 20}."
                f"{"0" * 100}"
            ),
        )

    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_400_BAD_REQUEST
