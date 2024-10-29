import pytest

from app.core.auth import jwt
from app.core.database.models import User


@pytest.fixture
def access_token(db_user: User, current_time: int) -> str:
    return jwt.generate_token(
        "access",
        user_id=db_user.id,
        email=db_user.email,
        current_time=current_time,
    )


@pytest.fixture
def refresh_token(db_user: User, current_time: int) -> str:
    return jwt.generate_token(
        "refresh",
        user_id=db_user.id,
        email=db_user.email,
        current_time=current_time,
    )
