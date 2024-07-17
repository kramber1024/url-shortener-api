from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .bases import IDBase

if TYPE_CHECKING:
    from app.core.database.models.user import User

    from .click import Click


class Link(IDBase):
    __tablename__ = "Links"

    user_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("Users.id"),
        primary_key=True,
        nullable=False,
    )
    address: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
    )
    location: Mapped[str] = mapped_column(
        String(512),
        nullable=False,
    )
    total_clicks: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
    )

    author: Mapped["User"] = relationship(
        "User",
        back_populates="links",
        lazy="selectin",
    )
    clicks: Mapped[list["Click"]] = relationship(
        "Click",
        back_populates="link",
        lazy="selectin",
    )

    def __init__(
        self,
        *,
        user_id: int,
        address: str,
        location: str,
    ) -> None:

        self.user_id = user_id
        self.address = address
        self.location = location
        self.total_clicks = 0
