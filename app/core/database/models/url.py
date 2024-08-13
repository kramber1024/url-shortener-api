from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.config import settings
from app.core.database.models.mixins import Base, IDMixin

if TYPE_CHECKING:
    from app.core.database.models import Click, Tag, User


class Url(Base, IDMixin):
    """Model for short URLs.

    Attributes
    ----------
        id (int): The unique identifier (See ` IDMixin `).
        user_id (int): The unique identifier of the ` User ` aka author.
        address (str): The short URL address.
        location (str): The long URL address.
        total_clicks (int): The total number of uses of the short URL.
        author (User): The author of the short URL.
        clicks (list[Click]): The list of ` Click`'s on the short URL.

    """

    __tablename__ = "Urls"

    user_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("Users.id"),
        primary_key=True,
        nullable=False,
    )
    address: Mapped[str] = mapped_column(
        String(settings.data.SHORT_URL_MAX_LENGTH),
        unique=True,
        nullable=False,
    )
    location: Mapped[str] = mapped_column(
        String(settings.data.URL_MAX_LENGTH),
        nullable=False,
    )
    total_clicks: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        lazy="selectin",
    )
    author: Mapped["User"] = relationship(
        "User",
        back_populates="urls",
        lazy="selectin",
    )
    clicks: Mapped[list["Click"]] = relationship(
        "Click",
        back_populates="url",
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

    def __repr__(self) -> str:
        return f"<{type(self).__name__} /{self.address} -> {self.location}>"
