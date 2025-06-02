from typing import Annotated

from pydantic import Field, StringConstraints

Id = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=len("7335256174294515712"),
        max_length=len("7335256174294515712"),
        pattern=r"^\d+$",
    ),
    Field(
        description="The unique identifier of the record.",
        examples=["7335256174294515712"],
    ),
]
