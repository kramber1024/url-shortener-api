from typing import TYPE_CHECKING, Final

import bcrypt
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.data import Email, FirstName, LastName, Password, Phone

from .mixins import CreatedAtMixin, IDMixin, TableNameMixin, UpdatedAtMixin
from .model import Model

if TYPE_CHECKING:
    from .status import Status
    from .url import Url

_SPLITTED_EMAIL_LENGTH: Final[int] = 2


class User(Model, TableNameMixin, IDMixin, UpdatedAtMixin, CreatedAtMixin):
    _first_name: Mapped[str] = mapped_column(
        "first_name",
        String(length=FirstName.MAX_LENGTH),
        nullable=False,
    )
    _last_name: Mapped[str | None] = mapped_column(
        "last_name",
        String(length=LastName.MAX_LENGTH),
        nullable=True,
    )
    _email: Mapped[str] = mapped_column(
        "email",
        String(length=Email.MAX_LENGTH),
        nullable=False,
        unique=True,
    )
    _phone: Mapped[str | None] = mapped_column(
        "phone",
        String(length=Phone.MAX_LENGTH),
        nullable=True,
        unique=True,
    )
    _password: Mapped[str] = mapped_column(
        "password",
        String(length=Password.HASHED_LENGTH),
        nullable=False,
    )

    status: Mapped["Status"] = relationship(
        "Status",
        lazy="selectin",
    )
    urls: Mapped[list["Url"]] = relationship(
        "Url",
        back_populates="author",
        lazy="selectin",
    )

    def __init__(
        self,
        *,
        first_name: str,
        last_name: str | None,
        email: str,
        password: str,
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = None
        self.password = password

    @hybrid_property
    def first_name(self) -> str:
        return self._first_name

    @first_name.setter
    def _first_name_setter(self, value: str) -> None:
        self._first_name = self._format_string(
            FirstName.MIN_LENGTH,
            FirstName.MAX_LENGTH,
            value,
        )

    @hybrid_property
    def last_name(self) -> str | None:
        return self._last_name

    @last_name.setter
    def _last_name_setter(self, value: str | None) -> None:
        if value is None:
            self._last_name = None
            return

        self._last_name = self._format_string(
            LastName.MIN_LENGTH,
            LastName.MAX_LENGTH,
            value,
        )

    @hybrid_property
    def email(self) -> str:
        return self._email

    @email.setter
    def _email_setter(self, value: str) -> None:
        splitted_value: list[str] = value.strip().split("@")

        if (
            len(splitted_value) != _SPLITTED_EMAIL_LENGTH
            or not Email.MIN_LENGTH
            <= len("@".join(splitted_value))
            <= Email.MAX_LENGTH
        ):
            raise ValueError

        self._email = f"{splitted_value[0]}@{splitted_value[1].lower()}"

    @hybrid_property
    def phone(self) -> str | None:
        return self._phone

    @phone.setter
    def _phone_setter(self, value: str | None) -> None:
        if value is None:
            self._phone = None
            return

        self._phone = self._format_string(
            Phone.MIN_LENGTH,
            Phone.MAX_LENGTH,
            value,
        )

    @hybrid_property
    def password(self) -> str:
        return self._password

    @password.setter
    def _password_setter(self, value: str) -> None:
        if not Password.MIN_LENGTH <= len(value) <= Password.MAX_LENGTH:
            raise ValueError

        self._password = self._hash_password(value, rounds=16)

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name or ""}".strip()

    def is_password_valid(self, password: str, /) -> bool:
        """Check if the password is valid for the user.

        Args:
            password (str): The password to check.

        Returns:
            bool: ` True ` if the password is valid, ` False ` otherwise.
        """
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=self.password.encode("utf-8"),
        )

    @staticmethod
    def _format_string(min_length: int, max_length: int, value: str, /) -> str:
        """Check the length of the string and return stripped version of it.

        Args:
            min_length (int): Minimum length of the string.
            max_length (int): Maximum length of the string.
            value (str): The string to format.

        Raises:
            ValueError: If the length of the string is not between
                        the min and max length.

        Returns:
            str: The stripped version of the string.
        """
        stripped_value: str = value.strip()

        if not (min_length <= len(stripped_value) <= max_length):
            raise ValueError

        return stripped_value

    @staticmethod
    def _hash_password(password: str, /, *, rounds: int) -> str:
        """Hash the password using bcrypt library.

        Args:
            password (str): The password to hash.
            rounds (int): The number of rounds to hash the password.

        Returns:
            str: The hashed password.
        """
        return bcrypt.hashpw(
            password.encode(encoding="utf-8"),
            bcrypt.gensalt(rounds=rounds, prefix=b"2b"),
        ).decode(encoding="utf-8")

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.display_name}>"
