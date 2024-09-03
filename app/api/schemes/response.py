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

_ErrorResponseMessage: TypeAlias = Annotated[
    str,
    Field(
        description="Generic error message.",
        examples=["Validation error"],
    ),
]

_SuccessResponseMessage: TypeAlias = Annotated[
    str,
    Field(
        description="Success message.",
        examples=["Operation completed successfully"],
    ),
]

_ErrorMessage: TypeAlias = Annotated[
    str,
    Field(
        description="Error message. Should not be used as feedback for a user.",
        examples=["Password length is incorrect"],
    ),
]

_ErrorType: TypeAlias = Annotated[
    str,
    Field(
        description=(
            "Error type. Should be used for frontend logic e.g. form validation."
        ),
        examples=["password"],
    ),
]


class Error(BaseModel):
    message: _ErrorMessage
    type: _ErrorType


_Errors: TypeAlias = Annotated[
    list[Error],
    Field(
        description="List of errors.",
    ),
]


class _BaseResponse(BaseModel):
    status: _HTTPStatus


class ErrorResponse(_BaseResponse):
    errors: _Errors
    message: _ErrorResponseMessage


class SuccessResponse(_BaseResponse):
    message: _SuccessResponseMessage
