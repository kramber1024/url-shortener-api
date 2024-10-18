from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins import Base, CreatedAtMixin, IDMixin

if TYPE_CHECKING:
    from .url import Url


class Click(Base, IDMixin, CreatedAtMixin):
    """Represents a click event on a shortened URL.

    Attributes:
        id (int): The unique identifier (See ` IDMixin `).
        url_id (int): The unique identifier of the `Url` to which this click event is
            related. A foreign key to the Urls table.
        ip (str | None): The IP address from which the click was made.
            Can be `None` if not available.
        country (str | None): The two-character [**ISO 3166-1 alpha-2 code**](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
            indicating the country from which the click originated.
            Can be `None` if the country is not identified by ` ip `.
        url (Url): The ` Url ` to which this click is associated.
            Establishes a relationship between the `Click` and the `Url` it belongs to.

    """

    __tablename__: str = "Clicks"

    url_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("Urls.id"),
        nullable=False,
    )
    ip: Mapped[str | None] = mapped_column(
        String(16),
        nullable=True,
    )
    country: Mapped[str | None] = mapped_column(
        String(2),
        nullable=True,
    )

    url: Mapped["Url"] = relationship(
        "Url",
        back_populates="clicks",
        lazy="selectin",
    )

    def __init__(
        self,
        *,
        url_id: int,
        ip: str | None,
        country: str | None,
    ) -> None:
        self.url_id = url_id
        self.ip = ip
        self.country = country
