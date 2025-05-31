from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import schemes

_ERRORS_MAP: dict[str, str] = {
    "string_pattern_mismatch": "The {} value is invalid",
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


def request_validation_error_handler(
    _request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors: list[schemes.Error] = []
    for error in exc.errors():
        message: str = _ERRORS_MAP.get(
            error["type"],
            f"Invalid value ({error['type']})",
        ).format(error["loc"][1])

        errors.append(
            schemes.Error(
                message=message,
                type=str(error["loc"][1]),
            ),
        )

    return JSONResponse(
        content=schemes.ErrorResponse(
            errors=errors,
            message="Validation error",
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        ).model_dump(mode="json"),
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def http_exception_handler(
    _request: Request,
    exc: HTTPException,
) -> JSONResponse:
    return JSONResponse(
        content=schemes.ErrorResponse(
            status=exc.status_code,
            errors=[],
            message=exc.detail,
        ).model_dump(mode="json"),
        status_code=exc.status_code,
    )


def exception_handler(
    _request: Request,
    _exc: Exception,
) -> JSONResponse:
    return JSONResponse(
        content=schemes.ErrorResponse(
            errors=[],
            message="Internal server error",
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ).model_dump(mode="json"),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
