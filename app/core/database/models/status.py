from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .mixins import Base, UpdatedAtMixin


class Status(Base, UpdatedAtMixin):
    """The status of a user, tracking their verification and membership details.

    Attributes:
        user_id (int): The unique identifier of the user.
            This is a foreign key linked to the Users table.
        email_verified (bool): Indicates whether the user's email address
            has been verified.
        phone_verified (bool): Indicates whether the user's phone number
            has been verified.
        active (bool): Indicates whether the user is currently active
            and allowed to log in.
        premium (bool): Indicates whether the user has a premium membership.
    """

    __tablename__: str = "Statuses"

    user_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("Users.id"),
        primary_key=True,
        nullable=False,
    )
    email_verified: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
    )
    phone_verified: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
    )
    active: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
    )
    premium: Mapped[bool] = mapped_column(
        Boolean(),
        nullable=False,
    )

    def __init__(
        self,
        *,
        user_id: int,
        active: bool = True,
        premium: bool = False,
    ) -> None:
        self.user_id = user_id
        self.email_verified = False
        self.phone_verified = False
        self.active = active
        self.premium = premium
