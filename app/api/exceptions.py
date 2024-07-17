from fastapi import HTTPException

from app.api.schemes import Error as ErrorScheme
from app.api.schemes import ErrorResponse as ErrorResponseScheme


# TODO(kramber): Improve naming of this class
# (Error exception??????????????)
# 000
class ErrorException(HTTPException):
    response: dict[str, str | int | list[dict[str, str]]]

    def __init__(self, errors: list[dict[str, str]], message: str, status: int) -> None:
        super().__init__(status_code=status, detail=message)

        errors_list: list[ErrorScheme] = [
            ErrorScheme(
                message=error["message"],
                type=error["type"],
            ) for error in errors
        ]

        self.response = ErrorResponseScheme(
            errors=errors_list,
            message=message,
            status=status,
        ).model_dump()
