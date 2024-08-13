from typing import Annotated, TypeAlias

from fastapi import status
from pydantic import BaseModel, Field

_HTTPStatus: TypeAlias = Annotated[
    int,
    Field(
        description="HTTP status code.",
        examples=[status.HTTP_422_UNPROCESSABLE_ENTITY],
        ge=100,
        le=599,
    ),
]


class Error(BaseModel):
    message: Annotated[
        str,
        Field(
            description="Error message. Should not be used as feedback for a user.",
            examples=["Password length is incorrect"],
        ),
    ]
    type: Annotated[
        str,
        Field(
            description=(
                "Error type. Should be used for frontend logic e.g. form validation."
            ),
            examples=["password"],
        ),
    ]


class ErrorResponse(BaseModel):
    errors: Annotated[
        list[Error],
        Field(
            description="List of errors.",
        ),
    ]
    message: Annotated[
        str,
        Field(
            description="Generic error message.",
            examples=["Validation error"],
        ),
    ]
    status: _HTTPStatus


class SuccessResponse(BaseModel):
    message: Annotated[
        str,
        Field(
            description="Success message.",
            examples=["Operation completed successfully"],
        ),
    ]
    status: _HTTPStatus
