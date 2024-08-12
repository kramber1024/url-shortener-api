from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.mixins import Base, IDMixin

if TYPE_CHECKING:
    from app.core.database.models import Url


class Tag(Base, IDMixin):
    """Model for short URL tags.

    Attributes
    ----------
        id (int): The unique identifier (See ` IDMixin `).
        url_id (int): The unique identifier of the ` Url `.
        name (str): The tag name. Used for categorization.
        url (Url): The ` Url ` the tag is associated with.

    """

    __tablename__ = "Tags"

    url_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("Urls.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    url: Mapped["Url"] = relationship(
        "Url",
        back_populates="tags",
        lazy="selectin",
    )

    def __init__(self, *, url_id: int, name: str) -> None:
        self.url_id = url_id
        self.name = name
