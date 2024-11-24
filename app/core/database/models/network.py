import ipaddress
from typing import Final

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .mixins import TableNameMixin
from .model import Model

_MAX_NETWORK_ADDRESS_LENGTH: Final[int] = len("255.255.255.255")


class Network(Model, TableNameMixin):
    """Model for network to country mapping.

    See [**ISO 3166-1**](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)

    Attributes:
        address (str): The network address.
        mask (int): The network mask.
        country (str): The ISO 3166-1 country code.
    """

    address: Mapped[str] = mapped_column(
        String(_MAX_NETWORK_ADDRESS_LENGTH),
        primary_key=True,
        nullable=False,
    )
    mask: Mapped[int] = mapped_column(
        Integer(),
        nullable=False,
    )
    country: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
    )

    def __init__(self, *, address: str, mask: int, country: str) -> None:
        self.address = address
        self.mask = mask
        self.country = country

    def __contains__(self, ip: str) -> bool:
        """Check if the given ` ip ` is in the network.

        Args:
            ip (str): The IP address to check. (See [**IPv4**](https://en.wikipedia.org/wiki/IPv4))

        Returns:
            bool: ` True ` if the ` ip ` is in the network, otherwise ` False `.
        """
        return ipaddress.ip_address(ip) in ipaddress.ip_network(
            f"{self.address}/{self.mask}",
        )

    def __str__(self) -> str:
        return f"{self.address}/{self.mask}"

    def __repr__(self) -> str:
        return f"<Network {self.address}/{self.mask} is {self.country}>"
