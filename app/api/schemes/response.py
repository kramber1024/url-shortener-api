from typing import Annotated, TypeAlias

from fastapi import status
from pydantic import BaseModel, Field

_HTTPStatus: TypeAlias = Annotated[
    int,
    Field(
        description="The HTTP status code for the response.",
        examples=[status.HTTP_422_UNPROCESSABLE_ENTITY],
        ge=100,
        le=599,
    ),
]

_ErrorResponseMessage: TypeAlias = Annotated[
    str,
    Field(
        description="A generic error message explaining the reason for the failure.",
        examples=["Validation error"],
    ),
]

_SuccessResponseMessage: TypeAlias = Annotated[
    str,
    Field(
        description=(
            "A message indicating that the operation was completed successfully."
        ),
        examples=["Operation completed successfully"],
    ),
]

_ErrorMessage: TypeAlias = Annotated[
    str,
    Field(
        description=(
            "A detailed error message. This should not be displayed directly to users."
        ),
        examples=["Password length is incorrect"],
    ),
]

_ErrorType: TypeAlias = Annotated[
    str,
    Field(
        description=(
            "The type of error, often corresponding to a form field or validation. "
            "Used by the frontend for handling specific logic."
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
        description="A list of specific errors encountered during the request.",
    ),
]


class _BaseResponse(BaseModel):
    status: _HTTPStatus


class ErrorResponse(_BaseResponse):
    errors: _Errors
    message: _ErrorResponseMessage


class SuccessResponse(_BaseResponse):
    message: _SuccessResponseMessage
