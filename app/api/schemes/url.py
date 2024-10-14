import string
from typing import Annotated, TypeAlias

import pydantic_core
from pydantic import (
    AfterValidator,
    BaseModel,
    Field,
    StringConstraints,
    UrlConstraints,
)

from app.core.config import settings
from app.core.database import models

from .fields import Id
from .tag import Tag, Tags

_URL_SAFE_CHARACTERS: str = string.ascii_letters + string.digits + "-_"


def _slug_characters_validator(value: str) -> str:
    if any(char not in _URL_SAFE_CHARACTERS for char in value):
        raise ValueError
    return value


_Slug: TypeAlias = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=settings.data.SHORT_URL_MIN_LENGTH,
        max_length=settings.data.SHORT_URL_MAX_LENGTH,
    ),
    AfterValidator(_slug_characters_validator),
    Field(
        description=(
            "A short URL address. If not provided by the user, it will be "
            "generated automatically."
        ),
        examples=["clickme"],
    ),
]


def _address_length_validator(
    value: pydantic_core.Url,
) -> str:
    if not (
        settings.data.URL_MIN_LENGTH <= len(str(value)) <= settings.data.URL_MAX_LENGTH
    ):
        raise ValueError
    return str(value)


_Address: TypeAlias = Annotated[
    pydantic_core.Url,
    UrlConstraints(
        max_length=settings.data.URL_MAX_LENGTH,
        allowed_schemes=["http", "https"],
    ),
    AfterValidator(_address_length_validator),
    Field(
        description="Long url to be shortened.",
        examples=["https://example.com/i-am-a-very-long-url"],
    ),
]

_TotalClicks: TypeAlias = Annotated[
    int,
    Field(
        description="Total number of clicks on the short URL.",
        examples=[123],
    ),
]

_Length: TypeAlias = Annotated[
    int,
    Field(description="Total number of urls in list", examples=[10]),
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
        description="Total number of URL's in a list.",
        examples=[123],
        min_length=0,
        max_length=settings.data.PREMIUM_USER_MAX_URL_AMOUNT,
    ),
]


class UrlList(BaseModel):
    urls: _Urls
    length: _Length

    @classmethod
    def from_model(cls: type["UrlList"], model: list[models.Url]) -> "UrlList":
        return cls(urls=[Url.from_model(url) for url in model], length=len(model))
