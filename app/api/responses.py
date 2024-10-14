from typing import Any, TypeAlias

from pydantic import BaseModel

from app.api import schemes

_Response: TypeAlias = dict[str, Any]


def response(
    *,
    description: str,
    model: type[BaseModel],
    example: dict[str, Any] | None = None,
) -> _Response:
    response: _Response = {
        "description": description,
        "model": model,
    }

    if example is not None:
        response.update(
            {
                "content": {
                    "application/json": {
                        "example": example,
                    },
                },
            },
        )

    return response


def validation_error_response(example: dict[str, Any]) -> _Response:
    return response(
        description=(
            "A validation error occurs when the input data provided does not meet the "
            "required scheme or format specified by the endpoint."
        ),
        model=schemes.ErrorResponse,
        example=example,
    )


UNAUTHORIZED: _Response = response(
    description="Authorization required. Provide a valid token in cookies.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Authorization required",
        "status": 401,
    },
)

INVALID_TOKEN: _Response = response(
    description="Provided token is not valid.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Invalid token",
        "status": 400,
    },
)

INTERNAL_SERVER_ERROR: _Response = response(
    description="Something went very wrong. Please report this issue.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Internal server error",
        "status": 500,
    },
)
