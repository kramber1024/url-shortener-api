from typing import Any

from pydantic import BaseModel

from app.api.schemes import ErrorResponse as ErrorResponseScheme

Response = dict[str, Any]


def response(
    description: str,
    model: type[BaseModel],
    example: dict[str, Any] | None = None,
) -> Response:
    response: Response = {
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


INVALID_TOKEN: Response = response(
    description="Provided token is not valid.",
    model=ErrorResponseScheme,
    example={
        "errors": [],
        "message": "Invalid token",
        "status": 400,
    },
)

INTERNAL_SERVER_ERROR: Response = response(
    description="Something went very wrong. Please report this issue.",
    model=ErrorResponseScheme,
    example={
        "errors": [],
        "message": "Internal server error",
        "status": 500,
    },
)
