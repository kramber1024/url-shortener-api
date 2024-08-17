from typing import Annotated, TypeAlias

import pydantic_core
from pydantic import (
    BaseModel,
    Field,
    StringConstraints,
    UrlConstraints,
    field_validator,
)

from app.api.schemes.fields import Id
from app.core.config import settings

_Address: TypeAlias = Annotated[
    str,
    Field(
        min_length=settings.data.SHORT_URL_MIN_LENGTH,
        max_length=settings.data.SHORT_URL_MAX_LENGTH,
        description=(
            "A short URL address. If not provided by the user, it will be "
            "generated automatically."
        ),
        examples=["clickme"],
    ),
]

_Location: TypeAlias = Annotated[
    pydantic_core.Url,
    UrlConstraints(
        max_length=settings.data.URL_MAX_LENGTH,
        allowed_schemes=["http", "https"],
    ),
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


class NewUrl(BaseModel):
    address: _Address | None = None
    location: _Location
    tags: _TagList | None = None

    @field_validator("location")
    @classmethod
    def validate_location_length(cls: type["NewUrl"], value: pydantic_core.Url) -> str:
        if len(str(value)) not in range(
            settings.data.URL_MIN_LENGTH,
            settings.data.URL_MAX_LENGTH + 1,
        ):
            raise ValueError
        return str(value)


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
