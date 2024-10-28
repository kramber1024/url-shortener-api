from app.core.database.models import User
from tests import testing_utils


def test_tablename() -> None:
    assert User.__tablename__ == "Users"


def test_init(user_credentials: User) -> None:
    user: User = User(
        first_name=user_credentials.first_name,
        last_name=user_credentials.last_name,
        email=testing_utils.USER_EMAIL,
        password=testing_utils.USER_PASSWORD,
    )

    assert user.first_name == user_credentials.first_name
    assert user.last_name == user_credentials.last_name
    assert user.email != testing_utils.USER_EMAIL
    assert user.email == testing_utils.format_email(testing_utils.USER_EMAIL)
    assert not user.phone
    assert user.password != testing_utils.USER_PASSWORD
    assert user.password.startswith("$2b$")


def test_display_name(user_credentials: User) -> None:
    user: User = User(
        first_name=user_credentials.first_name,
        last_name=user_credentials.last_name,
        email="",
        password="",
    )

    assert (
        user.display_name
        == f"{user_credentials.first_name} {user_credentials.last_name}"
    )


def test_display_name_no_last_name(user_credentials: User) -> None:
    user: User = User(
        first_name=user_credentials.first_name,
        last_name=None,
        email="",
        password="",
    )

    assert user.display_name == user_credentials.first_name


def test_is_password_valid() -> None:
    user: User = User(
        first_name="",
        last_name="",
        email="",
        password=testing_utils.USER_PASSWORD,
    )

    assert user.is_password_valid(
        password=testing_utils.USER_PASSWORD,
    )


def test_is_password_valid_failure() -> None:
    user: User = User(
        first_name="",
        last_name="",
        email="",
        password=testing_utils.USER_PASSWORD,
    )

    assert not user.is_password_valid(
        password=testing_utils.USER_PASSWORD[::-1],
    )


def test__format_email() -> None:
    assert User._format_email(
        testing_utils.USER_EMAIL,
    ) == testing_utils.format_email(
        testing_utils.USER_EMAIL,
    )


def test__format_email_uppercase() -> None:
    assert User._format_email(
        testing_utils.USER_EMAIL.upper(),
    ) == testing_utils.format_email(
        testing_utils.USER_EMAIL.upper(),
    )


def test__format_email_linvalid_email() -> None:
    email: str = "I_am_invalid_email"

    user: User = User(
        first_name="",
        last_name="",
        email=email,
        password="",
    )

    assert user.email == email


def test__hash_password() -> None:
    hashed_password: str = User._hash_password(testing_utils.USER_PASSWORD)

    assert hashed_password != testing_utils.USER_PASSWORD
    assert hashed_password.startswith("$2b$")


def test_repr(user_credentials: User) -> None:
    user: User = User(
        first_name=user_credentials.first_name,
        last_name=user_credentials.last_name,
        email="",
        password="",
    )

    assert (
        repr(user)
        == f"<User {user_credentials.first_name} {user_credentials.last_name}>"
    )


def test_repr_no_last_name(user_credentials: User) -> None:
    user: User = User(
        first_name=user_credentials.first_name,
        last_name=None,
        email="",
        password="",
    )

    assert repr(user) == f"<User {user_credentials.first_name}>"
