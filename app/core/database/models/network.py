from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .mixins import Base

_MAX_NETWORK_LENGTH = len("255.255.255.255")


class Network(Base):
    """Model for network to country mapping.

    Attributes:
        network (str): The network address.
        mask (int): The network mask.
        country (str): The country code.
    """

    __tablename__: str = "Networks"

    network: Mapped[str] = mapped_column(
        String(_MAX_NETWORK_LENGTH),
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
