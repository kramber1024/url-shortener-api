from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.core.settings.data import Name

from .mixins import CreatedAtMixin, IdMixin, TableNameMixin
from .model import Model
from .url import Url


class Tag(Model, TableNameMixin, IdMixin, CreatedAtMixin):
    """Model for ` Url ` tags."""

    _url_id: Mapped[int] = mapped_column(
        "url_id",
        ForeignKey(Url.id),
        nullable=False,
    )
    _name: Mapped[str] = mapped_column(
        "name",
        String(length=Name.MAX_LENGTH),
        nullable=False,
    )

    def __init__(self, *, url_id: int, name: str) -> None:
        """Initialize a ` Tag ` model instance.

        Arguments:
            url_id: The unique identifier of the ` Url ` the ` Tag ` is
                associated with.
            name: The ` Tag ` value.
        """
        self._url_id = url_id
        self.name = name

    @hybrid_property
    def url_id(self) -> int:
        """The unique identifier of the ` Url `."""
        return self._url_id

    @hybrid_property
    def name(self) -> str:
        """The ` Tag ` value."""
        return self._name

    @name.inplace.setter
    def _name_setter(self, value: str) -> None:
        if not Name.validate_length(value):
            raise ValueError

        self._name = value

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name}>"
