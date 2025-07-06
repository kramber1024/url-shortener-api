from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from app.core.database import models
from app.core.settings.data import Name


class Tag(BaseModel):
    name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=Name.MIN_LENGTH,
            max_length=Name.MAX_LENGTH,
        ),
        Field(
            description="A descriptive label for categorizing URLs.",
            examples=["python"],
        ),
    ]

    @classmethod
    def from_model(cls: type["Tag"], model: models.Tag) -> "Tag":
        return cls(name=model.name)
