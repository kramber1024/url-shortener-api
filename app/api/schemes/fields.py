from typing import Annotated, TypeAlias

from pydantic import Field

Id: TypeAlias = Annotated[
    str,
    Field(
        description="A unique identifier.",
        examples=["7205626878688008192"],
        max_length=len("7205626878688008192"),
        min_length=len("7205626878688008192"),
    ),
]
