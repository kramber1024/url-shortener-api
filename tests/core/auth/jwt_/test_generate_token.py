from typing import Any

import jwt
import pytest

from app.core.auth import jwt
from app.core.config import settings
from app.core.database.models import User
from tests import testing_utils


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

    decoded_header: dict[str, Any] = jwt.get_unverified_header(token)
    decoded_payload: Any = jwt.decode(
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
        current_time,
    )
    assert decoded_payload["iat"] == current_time
