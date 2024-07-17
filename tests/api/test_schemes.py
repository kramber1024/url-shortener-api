from app.api.schemes import User as UserScheme
from app.core.database.models import User as UserModel


def test_user_scheme() -> None:
    first_name: str = "Dillon"
    last_name: str = "Carroll"
    email: str = "Dovie87@gmail.com"
    password: str = "YzbXhViCSId_pJK"

    user_model: UserModel = UserModel(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )
    user_scheme: UserScheme = UserScheme.from_model(user_model)

    assert isinstance(user_scheme, UserScheme)
    assert user_scheme.id == str(user_model.id)
    assert user_scheme.first_name == user_model.first_name
    assert user_scheme.last_name == user_model.last_name
    assert user_scheme.email == user_model.email
