from sqlalchemy import ForeignKey, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.settings.data import IP, Country

from .mixins import CreatedAtMixin, IdMixin, TableNameMixin
from .model import Model
from .url import Url


class Click(Model, TableNameMixin, IdMixin, CreatedAtMixin):
    """Represents a click event on a shortened URL."""

    _url_id: Mapped[int] = mapped_column(
        "url_id",
        ForeignKey(Url.id),
        nullable=False,
    )
    _ip: Mapped[str | None] = mapped_column(
        "ip",
        String(length=IP.MAX_LENGTH),
        nullable=True,
    )
    _country: Mapped[str | None] = mapped_column(
        "country",
        String(length=Country.MAX_LENGTH),
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
        """Initialize a ` Click ` model instance.

        Args:
            url_id: The unique identifier of the ` Url ` the ` Click ` is
                associated with.
            ip: The IP address from which the ` Click ` was made.
            country: The two-letter country code of the origin of the ` Click `.
        """
        self._url_id = url_id
        self.ip = ip
        self.country = country

    @hybrid_property
    def url_id(self) -> int:
        """The unique identifier of the ` Url `."""
        return self._url_id

    @hybrid_property
    def ip(self) -> str | None:
        """The IP address from which the ` Click ` was made."""
        return self._ip

    @ip.inplace.setter
    def _ip_setter(self, value: str | None) -> None:
        if value is not None and not IP.validate_length(value):
            raise ValueError

        self._ip = value

    @hybrid_property
    def country(self) -> str | None:
        """The two-letter country code of the origin of the ` Click `."""
        return self._country

    @country.inplace.setter
    def _country_setter(self, value: str | None) -> None:
        if value is not None and not Country.validate_length(value):
            raise ValueError

        self._country = value

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.id} from {self.country}>"
