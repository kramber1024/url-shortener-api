from app.core.config import settings
from app.core.database.models import User
from tests import utils


def test_user_display_name() -> None:
    first_name: str = "Adonis"
    last_name: str = "Miller"

    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email="",
        password="",
    )

    assert user.display_name == f"{first_name} {last_name}"


def test_user_display_name_no_last_name() -> None:
    first_name: str = "Briana"

    user: User = User(
        first_name=first_name,
        last_name=None,
        email="",
        password="",
    )

    assert user.display_name == first_name


def test_is_password_valid_success() -> None:
    password: str = "XpRWZM113tlKo6v"

    user: User = User(
        first_name="",
        last_name="",
        email="",
        password=password,
    )

    assert user.is_password_valid(password=password)
    assert user.password != password


def test_is_password_valid_failure() -> None:
    password: str = "RLV_bzHRWN7s_et"

    user: User = User(
        first_name="",
        last_name="",
        email="",
        password=password,
    )

    assert not user.is_password_valid(password=password[::-1])


def test__format_email() -> None:
    email: str = "Harmony_Ebert4@gmail.com"

    user: User = User(
        first_name="",
        last_name="",
        email=email,
        password="",
    )

    assert user.email == email


def test__format_email_uppercase() -> None:
    email: str = "Reba41@gmail.com".upper()

    user: User = User(
        first_name="",
        last_name="",
        email=email,
        password="",
    )

    assert user.email == utils.format_email(email)


def test__format_email_linvalid_email() -> None:
    email: str = "Beatrice Leffler"

    user: User = User(
        first_name="",
        last_name="",
        email=email,
        password="",
    )

    assert user.email == email


def test__hash_password() -> None:
    password: str = "KDaN1dezEOWlNle"

    user: User = User(
        first_name="",
        last_name=None,
        email="",
        password=password,
    )

    assert user.password != password
    assert user.password.startswith(f"$2b${str(settings.db.SALT_ROUNDS).zfill(2)}$")


def test_user_repr() -> None:
    first_name: str = "Grayson"
    last_name: str = "Jaskolski"

    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email="",
        password="",
    )

    assert repr(user) == f"<User {first_name} {last_name}>"
