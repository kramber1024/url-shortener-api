from typing import Annotated, TypeAlias

from pydantic import BaseModel, Field, HttpUrl

from app.api.schemes.fields import Id

Address: TypeAlias = Annotated[
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

Location: TypeAlias = Annotated[
    HttpUrl,
    Field(
        min_length=1,
        max_length=2048,
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


TagList: TypeAlias = Annotated[
    list[Tag],
    Field(description="List of tags. Can be empty an empty list."),
]


class NewUrl(BaseModel):
    address: Address | None = None
    location: Location
    tags: TagList


class Url(BaseModel):
    id: Id
    address: Address
    location: Location
    total_clicks: Annotated[
        int,
        Field(
            description="Total number of clicks on the short URL.",
            examples=[123],
        ),
    ]
