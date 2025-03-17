import bcrypt
import pytest

from app.core.database.models import User
from app.core.settings.data import Email, FirstName, LastName, Phone
from app.core.settings.data.password import Password


@pytest.fixture(scope="module")
def first_name() -> str:
    return "John"


@pytest.fixture(scope="module")
def last_name() -> str:
    return "Doe"


@pytest.fixture(scope="module")
def email() -> str:
    return "john.doe@example.com"


@pytest.fixture(scope="module")
def password() -> str:
    return "password"


@pytest.fixture()
def user() -> User:
    return User(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password=__name__ * 4,
    )


@pytest.mark.parametrize(
    "first_name",
    ["John", "jane", "A" * FirstName.MAX_LENGTH],
)
@pytest.mark.parametrize(
    "last_name",
    ["Doe", "smith", None, "A" * LastName.MAX_LENGTH],
)
@pytest.mark.parametrize(
    "email",
    ["john.doe@example.com", "jane.smith@EXAMPLE.com"],
)
@pytest.mark.parametrize("password", ["password123", "anotherpassword"])
def test_user_init(
    first_name: str,
    last_name: str | None,
    email: str,
    password: str,
) -> None:
    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    assert user.first_name == first_name
    assert user.last_name == last_name
    assert user.email == f"{email.split('@')[0]}@{email.split('@')[1].lower()}"
    assert user.phone is None
    assert bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8"),
    )


@pytest.mark.parametrize(
    "first_name",
    ["John", "Jane", "A" * FirstName.MAX_LENGTH],
)
def test_user_property_first_name(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
) -> None:
    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    user.first_name = first_name

    assert user.first_name == first_name


@pytest.mark.parametrize(
    "first_name",
    ["John", "A" * FirstName.MIN_LENGTH, "A" * FirstName.MAX_LENGTH],
)
def test_user_property_first_name_setter(
    first_name: str,
    user: User,
) -> None:
    user.first_name = first_name

    assert user.first_name == first_name


@pytest.mark.parametrize(
    "first_name",
    ["", "A" * (FirstName.MAX_LENGTH + 1), "A" * (FirstName.MIN_LENGTH - 1)],
)
def test_user_property_first_name_setter_invalid_length(
    first_name: str,
    user: User,
) -> None:
    with pytest.raises(ValueError, match=".*"):
        user.first_name = first_name


@pytest.mark.parametrize(
    "last_name",
    ["Doe", "Smith", None, "A" * LastName.MAX_LENGTH],
)
def test_user_property_last_name(
    first_name: str,
    last_name: str | None,
    email: str,
    password: str,
) -> None:
    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    assert user.last_name == last_name


@pytest.mark.parametrize(
    "last_name",
    [
        "Doe",
        "Smith",
        None,
        "A" * LastName.MAX_LENGTH,
        "A" * LastName.MIN_LENGTH,
    ],
)
def test_user_property_last_name_setter(
    last_name: str | None,
    user: User,
) -> None:
    user.last_name = last_name

    assert user.last_name == last_name


@pytest.mark.parametrize(
    "last_name",
    ["", "A" * (LastName.MAX_LENGTH + 1), "A" * (LastName.MIN_LENGTH - 1)],
)
def test_user_property_last_name_setter_invalid_length(
    last_name: str,
    user: User,
) -> None:
    with pytest.raises(ValueError, match=".*"):
        user.last_name = last_name


@pytest.mark.parametrize(
    "email",
    ["john.doe@example.com", "jane.smith@Example.com"],
)
def test_user_property_email(
    first_name: str,
    last_name: str | None,
    email: str,
    password: str,
) -> None:
    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    assert user.email == f"{email.split('@')[0]}@{email.split('@')[1].lower()}"


@pytest.mark.parametrize(
    "email",
    ["john.doe@example.com", "jane.smith@ExamplE.com"],
)
def test_user_property_email_setter(
    email: str,
    user: User,
) -> None:
    user.email = email

    assert user.email == f"{email.split('@')[0]}@{email.split('@')[1].lower()}"


@pytest.mark.parametrize(
    "email",
    [
        "",
        "invalid-email",
        "a" * (Email.MAX_LENGTH + 1),
        "a" * (Email.MIN_LENGTH - 1),
    ],
)
def test_user_property_email_setter_invalid_length(
    email: str,
    user: User,
) -> None:
    with pytest.raises(ValueError, match=".*"):
        user.email = email


@pytest.mark.parametrize(
    "phone",
    ["1234567890", None, "1" * Phone.MAX_LENGTH, "1" * Phone.MIN_LENGTH],
)
def test_user_property_phone(
    first_name: str,
    last_name: str | None,
    email: str,
    password: str,
    phone: str | None,
) -> None:
    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )
    user.phone = phone

    assert user.phone == phone


@pytest.mark.parametrize(
    "phone",
    ["1234567890", "1" * Phone.MAX_LENGTH, "1" * Phone.MIN_LENGTH],
)
def test_user_property_phone_setter(
    phone: str | None,
    user: User,
) -> None:
    user.phone = phone

    assert user.phone == phone


@pytest.mark.parametrize(
    "phone",
    ["", "1" * (Phone.MAX_LENGTH + 1), "1" * (Phone.MIN_LENGTH - 1)],
)
def test_user_property_phone_setter_invalid_length(
    phone: str,
    user: User,
) -> None:
    with pytest.raises(ValueError, match=".*"):
        user.phone = phone


@pytest.mark.parametrize(
    "password",
    ["password123", "anotherpassword", "*&#^!(*@*&#$81)"],
)
def test_user_property_password(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
) -> None:
    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    assert user.password != password
    assert bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8"),
    )


@pytest.mark.parametrize(
    "password",
    ["password123", "anotherpassword", "*&#^!(*@*&#$81)"],
)
def test_user_property_password_setter(
    password: str,
    user: User,
) -> None:
    user.password = password

    assert user.password != password
    assert bcrypt.checkpw(
        password.encode("utf-8"),
        user.password.encode("utf-8"),
    )


@pytest.mark.parametrize(
    "password",
    [
        "",
        "1" * (Password.MIN_LENGTH - 1),
        "1" * (Password.MAX_LENGTH + 1),
    ],
)
def test_user_property_password_setter_invalid_length(
    password: str,
    user: User,
) -> None:
    with pytest.raises(ValueError, match=".*"):
        user.password = password


def test_user_property_display_name(user: User) -> None:
    assert user.display_name == "John Doe"


@pytest.mark.parametrize("password", ["password123", "anotherpassword"])
def test_user_is_password_valid(password: str, user: User) -> None:
    user.password = password

    assert user.is_password_valid(password) is True
    assert user.is_password_valid(password[::-1]) is False
    assert user.is_password_valid("wrongpassword") is False


def test_user_repr(user: User) -> None:
    assert repr(user) == f"<User {user.display_name}>"
