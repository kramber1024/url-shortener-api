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
    """Build a standardized OpenAPI response schema for documentation.

    Args:
        description: Human-readable explanation of the response scenario.
        model: The ` Pydantic ` model defining the response structure.
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


def unprocessable_entity_response(*, example: dict[str, Any]) -> dict[str, Any]:
    """Build a standardized OpenAPI response for validation errors.

    Args:
        example: JSON example showing validation error structure.

    Returns:
        A dictionary containing documentation.
    """
    return response(
        description="Input validation failed.",
        model=schemes.ErrorResponse,
        example=example,
    )


UNAUTHORIZED: dict[str, Any] = response(
    description="Authentication required. Provide a valid token in cookies.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Authentication required",
        "status": status.HTTP_401_UNAUTHORIZED,
    },
)

INVALID_TOKEN: dict[str, Any] = response(
    description="Authentication token is not valid.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Invalid token",
        "status": status.HTTP_400_BAD_REQUEST,
    },
)

INTERNAL_SERVER_ERROR: dict[str, Any] = response(
    description="Unexpected error occurred. Please report this issue.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Internal server error",
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
    },
)
