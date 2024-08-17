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

from app.api.schemes.fields import Id
from app.core.config import settings

_URL_SAFE_CHARACTERS: str = string.ascii_letters + string.digits + "-_"


def _address_characters_validator(value: str) -> str:
    if any(char not in _URL_SAFE_CHARACTERS for char in value):
        raise ValueError
    return value


_Address: TypeAlias = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=settings.data.SHORT_URL_MIN_LENGTH,
        max_length=settings.data.SHORT_URL_MAX_LENGTH,
    ),
    AfterValidator(_address_characters_validator),
    Field(
        description=(
            "A short URL address. If not provided by the user, it will be "
            "generated automatically."
        ),
        examples=["clickme"],
    ),
]


def _location_length_validator(
    value: pydantic_core.Url,
) -> str:
    if (
        len(str(value)) < settings.data.URL_MIN_LENGTH
        or len(str(value)) > settings.data.URL_MAX_LENGTH
    ):
        raise ValueError
    return str(value)


_Location: TypeAlias = Annotated[
    pydantic_core.Url,
    UrlConstraints(
        max_length=settings.data.URL_MAX_LENGTH,
        allowed_schemes=["http", "https"],
    ),
    AfterValidator(_location_length_validator),
    Field(
        description="Long url to be shortened.",
        examples=["https://example.com/i-am-a-very-long-url"],
    ),
]


class Tag(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=settings.data.TAG_MIN_LENGTH,
            max_length=settings.data.TAG_MAX_LENGTH,
        ),
        Field(
            description="Tag name.",
            examples=["python"],
        ),
    ]


_TagList: TypeAlias = Annotated[
    list[Tag],
    Field(
        description="Optional list of tags. Repeating tags will be ignored.",
        max_length=settings.data.SHORT_URL_MAX_TAGS_COUNT,
    ),
]


class CreateUrl(BaseModel):
    address: _Address | None = None
    location: _Location
    tags: _TagList | None = None


class Url(BaseModel):
    id: Id
    address: _Address
    location: _Location
    total_clicks: Annotated[
        int,
        Field(
            description="Total number of clicks on the short URL.",
            examples=[123],
        ),
    ]
