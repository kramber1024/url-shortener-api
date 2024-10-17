from typing import Annotated, TypeAlias

import pydantic_core
from pydantic import (
    BaseModel,
    Field,
    StringConstraints,
    UrlConstraints,
)

from app.core.config import settings
from app.core.database import models

from .fields import Id
from .tag import Tag, Tags

_Slug: TypeAlias = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=settings.data.SHORT_URL_MIN_LENGTH,
        max_length=settings.data.SHORT_URL_MAX_LENGTH,
        pattern=r"^[a-zA-Z0-9\-_]+$",
    ),
    Field(
        description=(
            "A custom or auto-generated identifier for the shortened "
            " URL. It must only contain letters, numbers, dashes, or underscores."
        ),
        examples=["clickme"],
    ),
]

_Address: TypeAlias = Annotated[
    pydantic_core.Url,
    UrlConstraints(
        max_length=settings.data.URL_MAX_LENGTH,
        allowed_schemes=["http", "https"],
    ),
    Field(
        description=(
            "The original URL that will be shortened. Must be a valid HTTP or HTTPS"
            " URL."
        ),
        examples=["https://example.com/i-am-a-very-long-url"],
    ),
]

_TotalClicks: TypeAlias = Annotated[
    int,
    Field(
        description="The total number of times the short URL has been accessed.",
        examples=[123],
        ge=0,
    ),
]

_Length: TypeAlias = Annotated[
    int,
    Field(
        description="The number of URLs in the list.",
        examples=[settings.data.FREE_USER_MAX_URL_AMOUNT - 1],
        ge=0,
        le=max(
            settings.data.FREE_USER_MAX_URL_AMOUNT,
            settings.data.PREMIUM_USER_MAX_URL_AMOUNT,
        ),
    ),
]


class _BaseUrl(BaseModel):
    tags: Tags
    address: _Address


class CreateUrl(_BaseUrl):
    slug: _Slug | None = None


class Url(_BaseUrl):
    id: Id
    slug: _Slug
    total_clicks: _TotalClicks

    @classmethod
    def from_model(cls: type["Url"], model: models.Url) -> "Url":
        return cls(
            id=str(model.id),
            total_clicks=model.total_clicks,
            slug=model.slug,
            address=pydantic_core.Url(model.address),
            tags=[Tag.from_model(tag) for tag in model.tags],
        )


_Urls: TypeAlias = Annotated[
    list[Url],
    Field(
        description="A collection of unique shortened URLs.",
        examples=[123],
        min_length=0,
        max_length=max(
            settings.data.FREE_USER_MAX_URL_AMOUNT,
            settings.data.PREMIUM_USER_MAX_URL_AMOUNT,
        ),
    ),
]


class UrlList(BaseModel):
    urls: _Urls
    length: _Length

    @classmethod
    def from_model(cls: type["UrlList"], model: list[models.Url]) -> "UrlList":
        return cls(urls=[Url.from_model(url) for url in model], length=len(model))
