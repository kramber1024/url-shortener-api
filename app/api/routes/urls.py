import base64
import secrets
import string
import time
from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import responses, schemes
from app.api.exceptions import HTTPError
from app.core.auth import jwt_
from app.core.config import settings
from app.core.database import db
from app.core.database.models import Url, User

router: APIRouter = APIRouter(
    prefix="/url",
    responses={
        status.HTTP_400_BAD_REQUEST: responses.INVALID_TOKEN,
        status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
    },
)


def _base10_to_urlsafe_base64(number: int) -> str:
    """Convert a base 10 number to a URL safe base 64 string.

    Args:
    ----
        number (int): The base 10 number to convert.

    Returns:
    -------
        str: The URL safe base 64 string.

    Examples:
    --------
    >>> url_safe_base64 = _base10_to_urlsafe_base64(123456789)
    >>> print(url_safe_base64)
    "B1vNFQ"

    """
    byte_representation: bytes = number.to_bytes(
        (number.bit_length() + 7) // 8,
        byteorder="big",
    )

    base64_encoded: bytes = base64.b64encode(byte_representation)

    return (
        base64_encoded.decode("utf-8").replace("+", "-").replace("/", "_").rstrip("=")
    )


async def _generate_url(*, session: AsyncSession) -> str:
    """Generate a random short url address.

    Args:
    ----
        session (AsyncSession): SQLAlchemy session object

    Raises:
    ------
        ValueError: Could not generate a unique short url address in a reasonable time.
        This exception is **very** unlikely to be raised.

    Returns:
    -------
        str: The generated short url address

    Examples:
    --------
    >>> short_url = await _generate_url(session=session)
    >>> print(address)
    "D6zLIi_y"

    """
    url_string: str = _base10_to_urlsafe_base64(
        int(f"{int(time.time())}{secrets.randbelow(9000) + 1000}"),
    )

    while len(url_string) < settings.data.SHORT_URL_MAX_LENGTH:
        url: Url | None = await crud.get_url_by_address(
            session=session,
            address=url_string,
        )

        if url is None:
            break

        url_string += secrets.choice(string.ascii_letters)

    else:
        value_error_message: str = (
            "Failed to generate a unique short url address in a reasonable time."
        )
        raise ValueError(value_error_message)

    return url_string


@router.post(
    "",
    summary="Create a new short url",
    description="Creates a new short url for the given long url.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: responses.response(
            description="Short url created successfully.",
            model=schemes.SuccessResponse,
            example={
                "message": "Short url created successfully",
                "status": status.HTTP_201_CREATED,
            },
        ),
        status.HTTP_409_CONFLICT: responses.response(
            description=(
                "Short url address already in use. User should use a different alias."
            ),
            model=schemes.ErrorResponse,
            example={
                "message": "Short url address already in use",
                "status": status.HTTP_409_CONFLICT,
            },
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: responses.validation_error_response(
            example={
                "errors": [],
                "message": "Validation error",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            },
        ),
    },
)
async def create_url(
    user: Annotated[
        User,
        Depends(jwt_.get_current_user),
    ],
    new_url: Annotated[
        schemes.NewUrl,
        Body(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
    ],
) -> JSONResponse:
    if new_url.address is not None and await crud.get_url_by_address(
        session=session,
        address=new_url.address,
    ):
        return JSONResponse(
            content={
                "message": "Short url address already in use",
                "status": status.HTTP_409_CONFLICT,
            },
            status_code=status.HTTP_409_CONFLICT,
        )

    if new_url.address is None:
        try:
            new_url.address = await _generate_url(session=session)

        except ValueError as e:
            raise HTTPError(
                errors=[],
                message=(
                    "Failed to generate a unique short url address in a reasonable time"
                ),
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            ) from e

    url: Url = await crud.create_url(
        session=session,
        user_id=user.id,
        address=new_url.address,
        location=str(new_url.location),
    )

    if new_url.tags is not None:
        tags_created: set[str] = set()

        for tag in new_url.tags:
            if tag.name in tags_created:
                continue

            await crud.create_tag(
                session=session,
                url_id=url.id,
                name=tag.name,
            )

            tags_created.add(tag.name)

    success_response: schemes.SuccessResponse = schemes.SuccessResponse(
        message="Url created successfully",
        status=status.HTTP_201_CREATED,
    )

    return JSONResponse(
        content=success_response.model_dump(),
        status_code=status.HTTP_201_CREATED,
    )
