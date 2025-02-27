from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.settings.data import Slug, Source

from .mixins import CreatedAtMixin, IdMixin, TableNameMixin, UpdatedAtMixin
from .model import Model
from .user import User

if TYPE_CHECKING:
    from .click import Click
    from .tag import Tag


class Url(Model, TableNameMixin, IdMixin, UpdatedAtMixin, CreatedAtMixin):
    """Model for shortened URL."""

    _user_id: Mapped[int] = mapped_column(
        "user_id",
        ForeignKey(User.id),
        nullable=False,
        primary_key=True,
    )
    _source: Mapped[str] = mapped_column(
        "source",
        String(length=Source.MAX_LENGTH),
        nullable=False,
    )
    _slug: Mapped[str] = mapped_column(
        "slug",
        String(length=Slug.MAX_LENGTH),
        nullable=False,
        unique=True,
    )
    _total_clicks: Mapped[int] = mapped_column(
        "total_clicks",
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
        source: str,
        slug: str,
    ) -> None:
        """Initialize a ` Url ` model instance.

        Args:
            user_id: The unique identifier of the ` User `.
            source: The original URL address.
            slug: The unique slug that identifies the shortened URL.
        """
        self._user_id = user_id
        self.source = source
        self.slug = slug
        self.total_clicks = 0

    @hybrid_property
    def user_id(self) -> int:
        """The unique identifier of the ` User `."""
        return self._user_id

    @hybrid_property
    def source(self) -> str:
        """The original URL address."""
        return self._source

    @source.inplace.setter
    def _source_setter(self, value: str) -> None:
        if not Source.validate_length(value):
            raise ValueError

        self._source = value

    @hybrid_property
    def slug(self) -> str:
        """The unique slug that identifies the shortened URL."""
        return self._slug

    @slug.inplace.setter
    def _slug_setter(self, value: str) -> None:
        if not Slug.validate_length(value):
            raise ValueError

        self._slug = value

    @hybrid_property
    def total_clicks(self) -> int:
        """The total number of ` Click `'s."""
        return self._total_clicks

    @total_clicks.inplace.setter
    def _total_clicks_setter(self, value: int) -> None:
        if value < 0:
            raise ValueError

        self._total_clicks = value

    def __repr__(self) -> str:
        return f"<{type(self).__name__} /{self.slug} -> {self.source}>"
