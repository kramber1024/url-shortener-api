from typing import Annotated

from fastapi import status
from pydantic import BaseModel, Field


class _BaseResponse(BaseModel):
    status: Annotated[
        int,
        Field(
            description=(
                "The HTTP status code indicating the outcome of the request."
            ),
            examples=[status.HTTP_422_UNPROCESSABLE_ENTITY],
            ge=100,
            le=599,
        ),
    ]


class Error(BaseModel):
    message: Annotated[
        str,
        Field(
            description=(
                "Technical error description for developers. Not intended for "
                "end-user display."
            ),
            examples=["Password length is incorrect"],
        ),
    ]
    type: Annotated[
        str,
        Field(
            description=(
                "The type of error, often corresponding to a form field or "
                "validation. Used by the frontend for handling specific logic."
            ),
            examples=["password"],
        ),
    ]


class ErrorResponse(_BaseResponse):
    errors: Annotated[
        list[Error],
        Field(
            description=(
                "Collection of specific validation or processing errors with "
                "type identifiers."
            ),
        ),
    ]
    message: Annotated[
        str,
        Field(
            description=(
                "A generic error message explaining the reason for the failure."
            ),
            examples=["Validation error"],
        ),
    ]


class SuccessResponse(_BaseResponse):
    message: Annotated[
        str,
        Field(
            description=(
                "A message indicating that the operation was completed "
                "successfully."
            ),
            examples=["Operation completed successfully"],
        ),
    ]
