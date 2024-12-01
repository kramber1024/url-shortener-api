from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.core.settings.data import Name

from .mixins import CreatedAtMixin, IDMixin, TableNameMixin
from .model import Model
from .url import Url


class Tag(Model, TableNameMixin, IDMixin, CreatedAtMixin):
    """Model for short ` URL ` tags."""

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
            url_id (int): The unique identifier of the ` Url `
                          ` Tag ` is associated with.
            name (str): The ` Tag ` value. Used for categorization.
        """
        self._url_id = url_id
        self.name = name

    @hybrid_property
    def url_id(self) -> int:
        """The unique identifier of the ` Url `.

        Returns:
            int: The unique identifier of the ` Url `.
        """
        return self._url_id

    @hybrid_property
    def name(self) -> str:
        """The ` Tag ` value. Used for categorization.

        Returns:
            str: The ` Tag ` value.
        """
        return self._name

    @name.inplace.setter
    def _name_setter(self, value: str) -> None:
        stripped_value: str = value.strip()

        if not Name.MIN_LENGTH <= len(stripped_value) <= Name.MAX_LENGTH:
            raise ValueError

        self._name = stripped_value

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.name}>"
