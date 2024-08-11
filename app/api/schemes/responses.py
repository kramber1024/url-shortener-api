from typing import Annotated

from pydantic import BaseModel, Field

from app.api.schemes.fields import HTTPStatus


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
    status: HTTPStatus


class SuccessResponse(BaseModel):
    message: Annotated[
        str,
        Field(
            description="Success message.",
            examples=["Operation completed successfully"],
        ),
    ]
    status: HTTPStatus


__all__ = (
    "Error",
    "ErrorResponse",
    "SuccessResponse",
)
