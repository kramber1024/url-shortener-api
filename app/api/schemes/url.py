from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    StringConstraints,
    UrlConstraints,
)

from app.core.config.data import Address, Slug, User
from app.core.database import models

from .fields import Id
from .tag import Tag

_Slug = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=Slug.MIN_LENGTH,
        max_length=Slug.MAX_LENGTH,
        pattern=r"^[a-zA-Z0-9\-_]+$",
    ),
    Field(
        description=(
            "A custom or auto-generated identifier for the shortened URL. "
            "It must only contain letters, numbers, dashes, or underscores."
        ),
        examples=["clickme"],
    ),
]


class CreateUrl(BaseModel):
    tags: Annotated[
        list[Tag],
        Field(
            description="A list of unique tags. Duplicate tags will be ignored",
            min_length=0,
            max_length=User.MAX_TAGS_PER_URL,
        ),
    ]
    slug: _Slug | None = None
    address: Annotated[
        HttpUrl,
        UrlConstraints(
            max_length=Address.MAX_LENGTH,
            allowed_schemes=["http", "https"],
        ),
        Field(
            description=(
                "The original URL that will be shortened. "
                "Must be a valid HTTP or HTTPS URL."
            ),
            examples=["https://example.com/i-am-a-very-long-url"],
        ),
    ]


class Url(CreateUrl):
    id: Id
    slug: _Slug
    total_clicks: Annotated[
        int,
        Field(
            description=(
                "The total number of times the short URL has been accessed."
            ),
            examples=[123],
            ge=0,
        ),
    ]

    @classmethod
    def from_model(cls: type["Url"], model: models.Url) -> "Url":
        return cls(
            id=str(model.id),
            total_clicks=model.total_clicks,
            slug=model.slug,
            address=HttpUrl(url=model.address),
            tags=[Tag.from_model(tag) for tag in model.tags],
        )


class UrlList(BaseModel):
    urls: Annotated[
        list[Url],
        Field(
            description="A collection of unique shortened URLs.",
            examples=[123],
            min_length=0,
            max_length=User.MAX_URL_AMOUNT,
        ),
    ]
    length: Annotated[
        int,
        Field(
            description="The number of URLs in the list.",
            examples=[6],
            ge=0,
            le=User.MAX_URL_AMOUNT,
        ),
    ]

    @classmethod
    def from_model(cls: type["UrlList"], model: list[models.Url]) -> "UrlList":
        return cls(
            urls=[Url.from_model(url) for url in model],
            length=len(model),
        )
