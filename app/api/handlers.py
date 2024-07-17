from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.exceptions import ErrorException
from app.api.schemes import Error as ErrorScheme
from app.api.schemes import ErrorResponse as ErrorResponseScheme


def validation_exception_handler(
    _: Request,
    exc: RequestValidationError | Exception,
) -> JSONResponse:

    errors_map: dict[str, str] = {
        "string_too_short": "The {} length is invalid",
        "string_too_long": "The {} length is invalid",
        "value_error": "The {} format is invalid",
        "missing": "The {} field is required",
        "string_type": "The {} should be a string",
        "json_invalid":  "Request should be a valid JSON",
        "literal_error": "The {} value is invalid",
    }
    errors: list[ErrorScheme] = []

    if isinstance(exc, RequestValidationError):
        for error in exc.errors():
            message: str = errors_map.get(
                error["type"],
                f"Invalid value ({error["type"]})",
            ).format(error["loc"][1])

            errors.append(
                ErrorScheme(
                    message=message,
                    type=str(error["loc"][1]),
                ),
            )

    else:
        errors.append(
            ErrorScheme(
                message="Iternal server error",
                type="server",
            ),
        )

    response: ErrorResponseScheme = ErrorResponseScheme(
        errors=errors,
        message="Validation error",
        status=422,
    )

    return JSONResponse(
        content=response.model_dump(),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def error_exception_handler(
    _: Request,
    exc: ErrorException | Exception,
) -> JSONResponse:

    if isinstance(exc, ErrorException):
        return JSONResponse(
            content=exc.response,
            status_code=exc.status_code,
        )

    server_error: ErrorException = ErrorException(
        errors=[],
        message="Internal server error",
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    return JSONResponse(
        content=server_error.response,
        status_code=server_error.status_code,
    )


def server_error_exception_handler(
    _: Request,
    __: Exception,
) -> JSONResponse:

    server_error: ErrorException = ErrorException(
        errors=[],
        message="Internal server error",
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )

    return JSONResponse(
        content=server_error.response,
        status_code=server_error.status_code,
    )
