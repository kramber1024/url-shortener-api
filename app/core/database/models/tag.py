from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.config import settings

from .mixins import CreatedAtMixin, IDMixin, TableNameMixin
from .model import Model
from .url import Url


class Tag(Model, TableNameMixin, IDMixin, CreatedAtMixin):
    """Model for short URL tags.

    Attributes:
        id (int): The unique identifier (See ` IDMixin `).
        url_id (int): The unique identifier of the ` Url `.
        name (str): The ` Tag ` name. Used for categorization.
        url (Url): The ` Url ` the tag is associated with.

    """

    url_id: Mapped[int] = mapped_column(
        ForeignKey(f"{Url.__tablename__}.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(settings.data.TAG_MAX_LENGTH),
        nullable=False,
    )

    def __init__(self, *, url_id: int, name: str) -> None:
        self.url_id = url_id
        self.name = name

    def __repr__(self) -> str:
        return f"<Tag {self.name} for ...>"
