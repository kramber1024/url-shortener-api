from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database.models.mixins import Base, IDMixin

if TYPE_CHECKING:
    from .url import Url


class Click(Base, IDMixin):
    __tablename__ = "Clicks"

    url_id: Mapped[int] = mapped_column(
        Integer(),
        ForeignKey("Urls.id"),
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

    url: Mapped["Url"] = relationship(
        "Url",
        back_populates="clicks",
        lazy="selectin",
    )

    def __init__(
        self,
        *,
        url_id: int,
        ip: str,
        country: str,
    ) -> None:
        self.url_id = url_id
        self.ip = ip
        self.country = country
