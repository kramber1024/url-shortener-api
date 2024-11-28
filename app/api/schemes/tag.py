from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from app.core.config.data import Name
from app.core.database import models


class Tag(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=Name.MIN_LENGTH,
            max_length=Name.MAX_LENGTH,
        ),
        Field(
            description=(
                "A tag associated with a URL. "
                "Used for categorization or labeling."
            ),
            examples=["python"],
        ),
    ]

    @classmethod
    def from_model(cls: type["Tag"], model: models.Tag) -> "Tag":
        return cls(
            name=model.name,
        )
