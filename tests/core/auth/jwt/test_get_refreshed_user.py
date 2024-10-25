import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import HTTPError
from app.core.auth import jwt
from app.core.database.models import User
from tests import testing_utils


@pytest.fixture
def refresh_token(db_user: User, current_time: int) -> str:
    return jwt.generate_token(
        "refresh",
        user_id=db_user.id,
        email=db_user.email,
        current_time=current_time,
    )


@pytest.mark.asyncio
async def test_get_refreshed_user(
    session: AsyncSession,
    refresh_token: str,
) -> None:
    refreshed_user: User = await jwt.get_refreshed_user(
        session=session,
        refresh_token=refresh_token,
    )

    assert refreshed_user
    assert refreshed_user.id in testing_utils.SNOWFLAKE_RANGE
    assert refreshed_user.first_name == testing_utils.USER_FIRST_NAME
    assert refreshed_user.last_name == testing_utils.USER_LAST_NAME
    assert refreshed_user.email == testing_utils.format_email(
        testing_utils.USER_EMAIL
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
async def test_get_refreshed_user_none_token(
    session: AsyncSession,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt.get_refreshed_user(
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
        await jwt.get_refreshed_user(
            session=session,
        )

    assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc.value.response.get("errors", "") == []
    assert exc.value.response.get("message", "")
    assert exc.value.response.get("status", 0) == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_refreshed_user_no_user(
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
        await jwt.get_refreshed_user(
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
    user_credentials: User,
) -> None:
    with pytest.raises(HTTPError) as exc:
        await jwt.get_refreshed_user(
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
