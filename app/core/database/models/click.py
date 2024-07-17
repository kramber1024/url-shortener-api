from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .bases import IDBase

if TYPE_CHECKING:
    from .link import Link


class Click(IDBase):
    __tablename__ = "Clicks"

    link_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("Links.id"),
        nullable=False,
    )
    ip: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
    )
    country: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    link: Mapped["Link"] = relationship(
        "Link",
        back_populates="clicks",
        lazy="selectin",
    )

    def __init__(
        self,
        *,
        link_id: int,
        ip: str,
        country: str,
    ) -> None:

        self.link_id = link_id
        self.ip = ip
        self.country = country
