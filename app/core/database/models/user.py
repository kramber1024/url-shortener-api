from typing import TYPE_CHECKING

import bcrypt
from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.settings import settings
from app.core.settings.data import Email, FirstName, LastName, Password, Phone

from .mixins import CreatedAtMixin, IdMixin, TableNameMixin, UpdatedAtMixin
from .model import Model

if TYPE_CHECKING:
    from .status import Status
    from .url import Url


class User(Model, TableNameMixin, IdMixin, UpdatedAtMixin, CreatedAtMixin):
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
        last_name: str | None = None,
        email: str,
        password: str,
    ) -> None:
        """Initialize a ` User ` model instance.

        Args:
            first_name: The ` User `'s first name.
            last_name: The ` User `'s last name. Defaults to None.
            email: The ` User `'s email address.
            password: The ` User `'s password.
        """
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = None
        self.password = password

    @hybrid_property
    def first_name(self) -> str:
        """The ` User `'s first name."""
        return self._first_name

    @first_name.inplace.setter
    def _first_name_setter(self, value: str) -> None:
        if not FirstName.validate_length(value):
            raise ValueError

        self._first_name = value

    @hybrid_property
    def last_name(self) -> str | None:
        """The ` User `'s last name."""
        return self._last_name

    @last_name.inplace.setter
    def _last_name_setter(self, value: str | None) -> None:
        if value is not None and not LastName.validate_length(value):
            raise ValueError

        self._last_name = value

    @hybrid_property
    def email(self) -> str:
        """The ` User `'s email address."""
        return self._email

    @email.inplace.setter
    def _email_setter(self, value: str) -> None:
        if not Email.validate_length(value) or "@" not in value:
            raise ValueError

        splitted_value: list[str] = value.strip().split("@")

        self._email = f"{splitted_value[0]}@{splitted_value[1].lower()}"

    @hybrid_property
    def phone(self) -> str | None:
        """The ` User `'s phone number."""
        return self._phone

    @phone.inplace.setter
    def _phone_setter(self, value: str | None) -> None:
        if value is not None and not Phone.validate_length(value):
            raise ValueError

        self._phone = value

    @hybrid_property
    def password(self) -> str:
        """The ` User `'s hashed password."""
        return self._password

    @password.inplace.setter
    def _password_setter(self, value: str) -> None:
        if not Password.validate_length(value):
            raise ValueError

        self._password = self._hash_password(
            value,
            rounds=settings.database.SALT_ROUNDS,
        )

    @property
    def display_name(self) -> str:
        """The ` User `'s display name."""
        return " ".join(filter(None, [self.first_name, self.last_name]))

    def is_password_valid(self, password: str, /) -> bool:
        """Check if the password is valid for the ` User `.

        Args:
            password: The password to check.

        Returns:
            ` True ` if the password is valid, ` False ` otherwise.
        """
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=self.password.encode("utf-8"),
        )

    @staticmethod
    def _hash_password(password: str, *, rounds: int) -> str:
        """Hash the password using bcrypt library.

        Args:
            password: The password to hash.
            rounds: The number of rounds to hash the password.

        Returns:
            The hashed password.
        """
        return bcrypt.hashpw(
            password.encode(encoding="utf-8"),
            bcrypt.gensalt(rounds=rounds, prefix=b"2b"),
        ).decode(encoding="utf-8")

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.display_name}>"
