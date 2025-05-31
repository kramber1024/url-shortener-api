from typing import Any

from fastapi import status
from pydantic import BaseModel

from app.api import schemes


def response(
    *,
    description: str,
    model: type[BaseModel],
    example: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Construct a standardized response for ` FastAPI ` endpoint documentation.

    Args:
        description: A brief description of the response.
        model: The ` Pydantic ` model that represents the response structure.
        example: Example JSON response data for documentation.

    Returns:
        A dictionary containing documentation.
    """
    response: dict[str, Any] = {
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


def validation_response(*, example: dict[str, Any]) -> dict[str, Any]:
    """Construct a standardized response for ` FastAPI ` validation errors.

    Args:
        example: Example JSON response data for documentation.

    Returns:
        A dictionary containing documentation.
    """
    return response(
        description="Request data validation failed.",
        model=schemes.ErrorResponse,
        example=example,
    )


UNAUTHORIZED: dict[str, Any] = response(
    description="Authorization required. Provide a valid token in cookies.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Authorization required",
        "status": status.HTTP_401_UNAUTHORIZED,
    },
)

INVALID_TOKEN: dict[str, Any] = response(
    description="Provided token is not valid.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Invalid token",
        "status": status.HTTP_400_BAD_REQUEST,
    },
)

INTERNAL_SERVER_ERROR: dict[str, Any] = response(
    description="Something went very wrong. Please report this.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Internal server error",
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
    },
)
