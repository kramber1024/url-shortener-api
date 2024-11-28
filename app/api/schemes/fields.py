from typing import Annotated

from pydantic import Field

Id = Annotated[
    str,
    Field(
        description="A unique identifier.",
        examples=["7205626878688008192"],
        max_length=len("7205626878688008192"),
        min_length=len("7205626878688008192"),
    ),
]
