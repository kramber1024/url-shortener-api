from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from .mixins import TableNameMixin, UpdatedAtMixin
from .model import Model
from .user import User


class Status(Model, TableNameMixin, UpdatedAtMixin):
    """The status of a ` User `."""

    _user_id: Mapped[int] = mapped_column(
        ForeignKey(User.id),
        nullable=False,
        primary_key=True,
    )
    _active: Mapped[bool] = mapped_column(
        "active",
        Boolean(),
        nullable=False,
    )
    _email_verified: Mapped[bool] = mapped_column(
        "email_verified",
        Boolean(),
        nullable=False,
    )
    _phone_verified: Mapped[bool] = mapped_column(
        "phone_verified",
        Boolean(),
        nullable=False,
    )

    def __init__(
        self,
        *,
        user_id: int,
        active: bool = True,
    ) -> None:
        """Initializes a new ` Status ` instance.

        Args:
            user_id: The unique identifier of the ` User `.
            active: Indicates whether the ` User ` is currently active. Defaults
                to ` True `.
        """
        self._user_id = user_id
        self.active = active
        self.email_verified = False
        self.phone_verified = False

    @hybrid_property
    def user_id(self) -> int:
        """The unique identifier of the ` User `."""
        return self._user_id

    @hybrid_property
    def active(self) -> bool:
        """Whether the ` User ` is currently active."""
        return self._active

    @active.inplace.setter
    def _active_setter(self, value: object) -> None:
        self._active = bool(value)

    @hybrid_property
    def email_verified(self) -> bool:
        """Whether the ` User `'s email address has been verified."""
        return self._email_verified

    @email_verified.inplace.setter
    def _email_verified_setter(self, value: object) -> None:
        self._email_verified = bool(value)

    @hybrid_property
    def phone_verified(self) -> bool:
        """Whether the ` User `'s phone number has been verified."""
        return self._phone_verified

    @phone_verified.inplace.setter
    def _phone_verified_setter(self, value: object) -> None:
        self._phone_verified = bool(value)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.user_id}>"
