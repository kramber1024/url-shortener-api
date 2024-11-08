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
from app.core.auth import jwt
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


def _base10_to_urlsafe_base64(number: int, /) -> str:
    """Convert a base 10 number to a URL safe base 64 string.

    Args:
        number (int): The base 10 number to convert.

    Returns:
        The URL safe base 64 string.

    Examples:
    >>> url_safe_base64 = (
    ...     base10_to_urlsafe_base64(
    ...         123456789
    ...     )
    ... )
    >>> print(url_safe_base64)
    "B1vNFQ"

    """
    byte_representation: bytes = number.to_bytes(
        (number.bit_length() + 7) // 8,
        byteorder="big",
    )

    base64_encoded: bytes = base64.b64encode(byte_representation)

    return (
        base64_encoded.decode("utf-8")
        .replace("+", "-")
        .replace("/", "_")
        .rstrip("=")
    )


async def _generate_unique_slug(
    *,
    session: AsyncSession,
    max_url_length: int,
    random_number: int | None = None,
    current_time: int,
) -> str:
    """Generate a random unique slug.

    Args:
        current_time (int): The current time in seconds since the epoch.
        session (AsyncSession): The database session.
        max_url_length (int): The maximum length of the slug.
        random_number (int | None, optional): A random number to allow for
                                              more then one slug per second.
                                              The bigger the number, the longer
                                              the slug. If None, a random
                                              number will be generated
                                              automatically. Defaults to None.

    Raises:
        ValueError: Failed to generate a unique slug in a reasonable time.

    Returns:
        str: A random unique slug.

    Example:
    >>> slug = await _generate_unique_slug(
    ...     current_time=utils.now(),
    ...     session=session,
    ...     max_url_length=16,
    ... )
    >>> print(slug)
    "KCvu2jY"
    """
    if random_number is None:
        random_number = secrets.randbelow(101)

    slug: str = _base10_to_urlsafe_base64(
        int(f"{current_time}{random_number}"),
    )
    while len(slug) < max_url_length:
        existing_url: Url | None = await crud.get_url_by_slug(
            session=session,
            slug=slug,
        )

        if existing_url is None:
            return slug

        slug += secrets.choice(string.ascii_letters)

    error_message: str = (
        "Failed to generate a unique slug in a reasonable time."
    )

    raise ValueError(
        error_message,
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
                "Slug is already in use. User should use a different alias."
            ),
            model=schemes.ErrorResponse,
            example={
                "message": "Slug is already in use",
                "status": status.HTTP_409_CONFLICT,
            },
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: responses.validation_response(
            example={
                "errors": [],
                "message": "Validation error",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            },
        ),
        status.HTTP_503_SERVICE_UNAVAILABLE: responses.response(
            description=(
                "Failed to generate a unique slug in a reasonable time. "
                "This error is pretty much **impossible** to happen."
            ),
            model=schemes.ErrorResponse,
            example={
                "message": (
                    "Failed to generate a unique slug in a reasonable time"
                ),
                "status": status.HTTP_503_SERVICE_UNAVAILABLE,
            },
        ),
    },
)
async def create_url(
    user: Annotated[
        User,
        Depends(jwt.current_user),
    ],
    create_url: Annotated[
        schemes.CreateUrl,
        Body(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
    ],
) -> JSONResponse:
    if create_url.slug is not None and await crud.get_url_by_slug(
        session=session,
        slug=create_url.slug,
    ):
        return JSONResponse(
            content={
                "message": "Slug is already in use",
                "status": status.HTTP_409_CONFLICT,
            },
            status_code=status.HTTP_409_CONFLICT,
        )

    if create_url.slug is None:
        try:
            create_url.slug = await _generate_unique_slug(
                session=session,
                max_url_length=settings.data.SHORT_URL_MAX_LENGTH,
                current_time=utils.now(),
            )
        except ValueError as error:
            raise HTTPError(
                errors=[],
                message="Failed to generate a unique slug in a reasonable time",
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            ) from error

    url: Url = await crud.create_url(
        session=session,
        user_id=user.id,
        slug=create_url.slug,
        address=str(create_url.address),
    )

    tag_names: set[str] = {tag.name for tag in create_url.tags}
    for tag_name in tag_names:
        await crud.create_tag(
            session=session,
            url_id=url.id,
            name=tag_name,
        )

    return JSONResponse(
        content=schemes.SuccessResponse(
            message="Url created successfully",
            status=status.HTTP_201_CREATED,
        ).model_dump(mode="json"),
        status_code=status.HTTP_201_CREATED,
    )
