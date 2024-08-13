from typing import Annotated, TypeAlias

import pydantic_core
from pydantic import BaseModel, Field, HttpUrl, field_validator

from app.api.schemes.fields import Id

_Address: TypeAlias = Annotated[
    str,
    Field(
        min_length=1,
        max_length=256,
        description=(
            "A short URL address. If not provided by the user, it will be "
            "generated automatically."
        ),
        examples=["clickme"],
    ),
]

_Location: TypeAlias = Annotated[
    HttpUrl,
    Field(
        description="Long url to be shortened.",
        examples=["https://example.com/i-am-a-very-long-url"],
    ),
]


class Tag(BaseModel):
    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=32,
            description="Tag name.",
            examples=["python"],
        ),
    ]


_TagList: TypeAlias = Annotated[
    list[Tag],
    Field(
        description="Optional list of tags. Repeating tags will be ignored.",
        max_length=32,
    ),
]


class NewUrl(BaseModel):
    address: _Address | None = None
    location: _Location
    tags: _TagList | None = None

    @field_validator("location")
    @classmethod
    def validate_location_length(cls: type["NewUrl"], value: pydantic_core.Url) -> str:
        if len(str(value)) not in range(1, 2049):
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
