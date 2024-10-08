from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .mixins import Base

_MAX_NETWORK_ADDRESS_LENGTH: int = len("255.255.255.255")


class Network(Base):
    """Model for network to country mapping.

    Attributes:
        address (str): The network address.
        mask (int): The network mask.
        country (str): The country code. \
            (See [**ISO 3166-1 alpha-2**](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2))
    """

    __tablename__: str = "Networks"

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

    def __repr__(self) -> str:
        return f"<Network {self.address}/{self.mask} is {self.country}>"
