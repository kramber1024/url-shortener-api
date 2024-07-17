from sqlalchemy import Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .bases import Base


class Status(Base):
    __tablename__ = "Statuses"

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
