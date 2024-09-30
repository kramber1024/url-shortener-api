from typing import Annotated, TypeAlias

from pydantic import BaseModel, Field, StringConstraints

from app.core.config import settings
from app.core.database import models

_Name: TypeAlias = Annotated[
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


class Tag(BaseModel):
    name: _Name

    @classmethod
    def from_model(cls: type["Tag"], model: models.Tag) -> "Tag":
        return cls(
            name=model.name,
        )


TagList: TypeAlias = Annotated[
    list[Tag],
    Field(
        description="Repeating tags will be ignored. Can be empty.",
        min_length=0,
        max_length=settings.data.SHORT_URL_MAX_TAGS_COUNT,
    ),
]
