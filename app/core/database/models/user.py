from typing import TYPE_CHECKING

import bcrypt
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.core.database.models.mixins import Base, IDMixin

if TYPE_CHECKING:
    from app.core.database.models import Status, Url

_HASHED_PASSWORD_MAX_LENGTH: int = 64


class User(Base, IDMixin):
    __tablename__ = "Users"

    first_name: Mapped[str] = mapped_column(
        String(settings.data.FIRST_NAME_MAX_LENGTH),
        nullable=False,
    )
    last_name: Mapped[str | None] = mapped_column(
        String(settings.data.LAST_NAME_MAX_LENGTH),
        nullable=True,
    )
    email: Mapped[str] = mapped_column(
        String(settings.data.EMAIL_MAX_LENGTH),
        nullable=False,
        unique=True,
    )
    phone: Mapped[str | None] = mapped_column(
        String(settings.data.PHONE_MAX_LENGTH),
        nullable=True,
    )
    password: Mapped[str] = mapped_column(
        String(_HASHED_PASSWORD_MAX_LENGTH),
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
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = self._format_email(email)
        self.phone = None
        self.password = self._hash_password(password)

    @property
    def display_name(self) -> str:
        return f"{self.first_name} {self.last_name or ""}".strip()

    def is_password_valid(self, password: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            self.password.encode("utf-8"),
        )

    @staticmethod
    def _format_email(email: str) -> str:
        if "@" not in email:
            return email

        email_splitted: list[str] = email.split("@")
        return f"{email_splitted[0]}@{email_splitted[1].lower()}"

    @staticmethod
    def _hash_password(password: str) -> str:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(rounds=settings.db.SALT_ROUNDS),
        ).decode("utf-8")

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.display_name}>"
