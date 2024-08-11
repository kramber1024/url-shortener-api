from app.api import schemes
from app.core.database import models


def test_user_scheme() -> None:
    first_name: str = "Dillon"
    last_name: str = "Carroll"
    email: str = "Dovie87@gmail.com"
    password: str = "YzbXhViCSId_pJK"

    user_model: models.User = models.User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )
    user_scheme: schemes.User = schemes.User.from_model(user_model)

    assert isinstance(user_scheme, schemes.User)
    assert user_scheme.id == str(user_model.id)
    assert user_scheme.first_name == user_model.first_name
    assert user_scheme.last_name == user_model.last_name
    assert user_scheme.email == user_model.email
