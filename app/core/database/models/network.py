from ipaddress import IPv4Network

from sqlalchemy import BigInteger, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column

from app.core.settings.data import Country

from .mixins import CreatedAtMixin, TableNameMixin
from .model import Model


class Network(Model, TableNameMixin, CreatedAtMixin):
    """Model for network to country mapping."""

    _id: Mapped[int] = mapped_column(
        "id",
        Integer(),
        nullable=False,
        primary_key=True,
        autoincrement=True,
    )
    _start_address: Mapped[int] = mapped_column(
        "start_address",
        BigInteger(),
        nullable=False,
    )
    _end_address: Mapped[int] = mapped_column(
        "end_address",
        BigInteger(),
        nullable=False,
    )
    _country: Mapped[str] = mapped_column(
        "country",
        String(length=Country.MAX_LENGTH),
        nullable=False,
    )

    def __init__(self, *, address: str, mask: int, country: str) -> None:
        """Initialize a ` Network ` model instance.

        Args:
            address: The ` Network ` address.
            mask: The ` Network ` mask.
            country: The ISO 3166-1 country code.

        Raises:
            ValueError: If the input values are invalid.
        """
        network: IPv4Network = IPv4Network(f"{address}/{mask}")

        if not Country.validate_length(country) or not country.isalpha():
            raise ValueError

        self._start_address = int(network.network_address)
        self._end_address = int(network.broadcast_address)
        self._country = country

    @hybrid_property
    def id(self) -> int:
        """The auto-incremented identifier."""
        return self._id

    @hybrid_property
    def start_address(self) -> int:
        """The start address of the ` Network `."""
        return self._start_address

    @hybrid_property
    def end_address(self) -> int:
        """The end address of the ` Network `."""
        return self._end_address

    @hybrid_property
    def country(self) -> str:
        """The ISO 3166-1 country code.

        See [**ISO 3166-1**](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2).
        """
        return self._country

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.country}>"
