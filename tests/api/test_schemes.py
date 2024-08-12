from app.api import schemes
from app.core.database import models


def test_user_scheme(user_credentials: models.User) -> None:
    user_scheme: schemes.User = schemes.User.from_model(user_credentials)

    assert isinstance(user_scheme, schemes.User)
    assert user_scheme.id == str(user_credentials.id)
    assert user_scheme.first_name == user_credentials.first_name
    assert user_scheme.last_name == user_credentials.last_name
    assert user_scheme.email == user_credentials.email
