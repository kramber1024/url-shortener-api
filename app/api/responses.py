from typing import Any, TypeAlias

from fastapi import status
from pydantic import BaseModel

from app.api import schemes

_Response: TypeAlias = dict[str, Any]


def response(
    *,
    description: str,
    model: type[BaseModel],
    example: dict[str, Any] | None = None,
) -> _Response:
    """Constructs a standardized response object for documenting API endpoints.

    Args:
        description (str): A brief description of the response.
        model (type[BaseModel]): The Pydantic model that represents the
                                 response structure.
        example (dict[str, Any] | None, optional): Example of a endpoint JSON
                                                   response. Optional.

    Returns:
        _Response: A dictionary-like response object that includes
                   the description, model, and example (if provided).
                   Should be used for ` responses ` dict of an endpoint.
    """
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


def validation_response(*, example: dict[str, Any]) -> _Response:
    """Constructs a standardized response object for documenting 422 error.

    Args:
        example (dict[str, Any]): Example of a endpoint JSON response.

    Returns:
        _Response: A dictionary-like response object that includes
                   the description, model, and example. Should be
                   used for documenting 422 error of an endpoint.
    """
    return response(
        description=(
            "A validation error occurs when the input data provided does not "
            "meet the required scheme or format specified by the endpoint."
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
        "status": status.HTTP_401_UNAUTHORIZED,
    },
)

INVALID_TOKEN: _Response = response(
    description="Provided token is not valid.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Invalid token",
        "status": status.HTTP_400_BAD_REQUEST,
    },
)

INTERNAL_SERVER_ERROR: _Response = response(
    description="Something went very wrong. Please report this.",
    model=schemes.ErrorResponse,
    example={
        "errors": [],
        "message": "Internal server error",
        "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
    },
)
