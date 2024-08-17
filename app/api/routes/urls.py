import base64
import secrets
import string
from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import responses, schemes
from app.api.exceptions import HTTPError
from app.core import utils
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
        number (int): The base 10 number to convert.

    Returns:
        str: The URL safe base 64 string.

    Examples:
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


def _generate_url(*, current_time: int, random_number: int | None = None) -> str:
    """Generate a random short url address.

    Args:
        current_time (int): The current time in seconds since the epoch.
        random_number (int | None, optional): A random number to allow for more then\
        one short url per second. The bigger the number, the longer the address.\
        If None, a random number will be generated automatically. Defaults to None.

    Returns:
        str: Random short url address

    Examples:
    >>> short_url = _generate_url(current_time=1620000000, random_number=123)
    >>> print(address)
    "AXkvhkh7"

    """
    if random_number is None:
        random_number = secrets.randbelow(101)

    return _base10_to_urlsafe_base64(
        int(f"{current_time}{random_number}"),
    )


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
        status.HTTP_503_SERVICE_UNAVAILABLE: responses.response(
            description=(
                "Failed to generate a unique short url address in a reasonable time. "
                "This error is pretty much **impossible** to happen."
            ),
            model=schemes.ErrorResponse,
            example={
                "message": (
                    "Failed to generate a unique short url address in a reasonable time"
                ),
                "status": status.HTTP_503_SERVICE_UNAVAILABLE,
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
        url_string: str = _generate_url(current_time=utils.now())

        while len(url_string) < settings.data.SHORT_URL_MAX_LENGTH:
            existing_url: Url | None = await crud.get_url_by_address(
                session=session,
                address=url_string,
            )

            if existing_url is None:
                new_url.address = url_string
                break

            url_string += secrets.choice(string.ascii_letters)

        else:
            raise HTTPError(
                errors=[],
                message=(
                    "Failed to generate a unique short url address in a reasonable time"
                ),
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

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
