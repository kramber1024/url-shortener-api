from typing import Any

from pydantic import BaseModel

from app.api.schemes import ErrorResponse as ErrorResponseScheme

_response = dict[str, Any]


def response(
    description: str,
    model: type[BaseModel],
    example: dict[str, Any] | None = None,
) -> _response:
    response: _response = {
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


def validation_error_response(example: dict[str, Any]) -> _response:
    return response(
        description=(
            "A validation error occurs when the input data provided does not meet the "
            "required scheme or format specified by the endpoint."
        ),
        model=ErrorResponseScheme,
        example=example,
    )


INVALID_TOKEN: _response = response(
    description="Provided token is not valid.",
    model=ErrorResponseScheme,
    example={
        "errors": [],
        "message": "Invalid token",
        "status": 400,
    },
)

INTERNAL_SERVER_ERROR: _response = response(
    description="Something went very wrong. Please report this issue.",
    model=ErrorResponseScheme,
    example={
        "errors": [],
        "message": "Internal server error",
        "status": 500,
    },
)
