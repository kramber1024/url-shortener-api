from typing import TypeAlias, TypedDict

from fastapi import HTTPException

from app.api import schemes


class _ErrorDict(TypedDict):
    message: str
    type: str


_Response: TypeAlias = dict[str, str | int | list[_ErrorDict]]


class HTTPError(HTTPException):
    """Custom wrapper for ` HTTPException ` from FastAPI.

    Based on ` ErrorResponse ` from schemes.

    Args:
        errors (list[_ErrorDict]): List of errors.
        message (str): Generic error message.
        status (int): HTTP status code.
        headers (dict[str, str] | None): Headers for response.

    Attributes:
        response (_Response): JSON response.

    Examples:
        >>> raise HTTPError(
        ...     errors=[
        ...         {
        ...             "message": "The password field is required",
        ...             "type": "password",
        ...         },
        ...     ],
        ...     message="Validation error",
        ...     status=422,
        ... )

    """

    response: _Response

    def __init__(
        self,
        *,
        errors: list[_ErrorDict],
        message: str,
        status: int,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status,
            detail=message,
            headers=headers,
        )

        errors_list: list[schemes.Error] = [
            schemes.Error(
                message=error["message"],
                type=error["type"],
            )
            for error in errors
        ]

        self.response = schemes.ErrorResponse(
            errors=errors_list,
            message=message,
            status=status,
        ).model_dump()
