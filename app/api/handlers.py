from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import schemes
from app.api.exceptions import HTTPError


def request_validation_error_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors_map: dict[str, str] = {
        "string_too_short": "The {} length is invalid",
        "string_too_long": "The {} length is invalid",
        "string_type": "The {} should be a string",
        "literal_error": "The {} value is invalid",
        "value_error": "The {} format is invalid",
        "json_invalid": "Request should be a valid JSON",
        "missing": "The {} field is required",
        "url_parsing": "The {} format is invalid",
        "url_too_long": "The {} length is invalid",
    }
    errors: list[schemes.Error] = []

    for error in exc.errors():
        message: str = errors_map.get(
            error["type"],
            f"Invalid value ({error["type"]})",
        ).format(error["loc"][1])

        errors.append(
            schemes.Error(
                message=message,
                type=str(error["loc"][1]),
            ),
        )

    response: schemes.ErrorResponse = schemes.ErrorResponse(
        errors=errors,
        message="Validation error",
        status=422,
    )

    return JSONResponse(
        content=response.model_dump(),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def http_error_handler(
    _: Request,
    exc: HTTPError,
) -> JSONResponse:
    return JSONResponse(
        content=exc.response,
        status_code=exc.status_code,
    )


def exception_handler(
    _: Request,
    __: Exception,
) -> JSONResponse:
    return JSONResponse(
        content=schemes.ErrorResponse(
            errors=[],
            message="Internal server error",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ).model_dump(),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
