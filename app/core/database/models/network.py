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
        try:
            network: IPv4Network = IPv4Network(f"{address}/{mask}")
        except ValueError as value_error:
            message: str = (
                f"'{address}/{mask}' does not appear to be an IPv4 network"
            )
            raise ValueError(message) from value_error

        if not Country.validate_length(country) or not country.isalpha():
            message = f"Invalid country code '{country}'"
            raise ValueError(message)

        self._start_address = int(network.network_address)
        self._end_address = int(network.broadcast_address)
        self._country = country
        self._address = address
        self._mask = mask

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

    @property
    def address(self) -> str:
        """The ` Network ` address."""
        return self._address

    @property
    def mask(self) -> int:
        """The ` Network ` mask."""
        return self._mask

    @property
    def cidr(self) -> str:
        """The CIDR representation of the ` Network `."""
        return f"{self.address}/{self.mask}"

    def __repr__(self) -> str:
        return f"<{type(self).__name__} {self.cidr} {self.country}>"
