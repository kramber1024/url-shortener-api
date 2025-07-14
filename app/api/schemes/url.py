from typing import Annotated

from pydantic import (
    BaseModel,
    Field,
    HttpUrl,
    StringConstraints,
    UrlConstraints,
)

from app.core.database import models
from app.core.settings.data import Slug, Source, User

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
    source: Annotated[
        HttpUrl,
        UrlConstraints(
            max_length=Source.MAX_LENGTH,
            allowed_schemes=["http", "https"],
        ),
        Field(
            description=(
                "The original URL that will be shortened. Must be a valid "
                "HTTP or HTTPS URL."
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
            source=HttpUrl(url=model.source),
            tags=[Tag.from_model(tag) for tag in model.tags],
        )
