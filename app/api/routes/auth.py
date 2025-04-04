from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import responses, schemes
from app.api.exceptions import HTTPError
from app.core import utils
from app.core.auth import jwt
from app.core.auth.jwt import TokenType
from app.core.database import database
from app.core.database.models import User
from app.core.settings import settings

router: APIRouter = APIRouter(prefix="/auth")


@router.post(
    "/register",
    summary="Create a new user account",
    description="Registers new user account in the system.",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: responses.response(
            description="New user account registered successfully.",
            model=schemes.SuccessResponse,
            example={
                "message": "Account created successfully",
                "status": status.HTTP_201_CREATED,
            },
        ),
        status.HTTP_409_CONFLICT: responses.response(
            description=(
                "The email is already in use. "
                "User should use a different email or login."
            ),
            model=schemes.ErrorResponse,
            example={
                "errors": [],
                "message": "The email is already in use",
                "status": status.HTTP_409_CONFLICT,
            },
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: responses.validation_response(
            example={
                "errors": [
                    {
                        "message": "The last_name length is invalid",
                        "type": "last_name",
                    },
                    {
                        "message": "The email format is invalid",
                        "type": "email",
                    },
                    {
                        "message": "The password field is required",
                        "type": "password",
                    },
                ],
                "message": "Validation error",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            },
        ),
    },
)
async def register_user(
    create_user: Annotated[
        schemes.CreateUser,
        Body(),
    ],
    async_session: Annotated[
        AsyncSession,
        Depends(database.get_async_session),
    ],
) -> JSONResponse:
    if await crud.get_user_by_email(
        async_session=async_session,
        email=create_user.email,
    ):
        raise HTTPError(
            errors=[],
            message="The email is already in use",
            status=status.HTTP_409_CONFLICT,
        )

    user: User = await crud.create_user(
        async_session=async_session,
        first_name=create_user.first_name,
        last_name=create_user.last_name,
        email=create_user.email,
        password=create_user.password,
    )
    await crud.create_status(
        async_session=async_session,
        user_id=user.id,
        active=True,
        premium=False,
    )

    return JSONResponse(
        content=schemes.SuccessResponse(
            message="Account created successfully",
            status=status.HTTP_201_CREATED,
        ).model_dump(mode="json"),
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/login",
    summary="Authenticate user",
    description="Authenticates a user in the system using email and password.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: responses.response(
            description="User authenticated successfully.",
            model=schemes.SuccessResponse,
            example={
                "message": "User authenticated successfully",
                "status": status.HTTP_200_OK,
            },
        ),
        status.HTTP_401_UNAUTHORIZED: responses.response(
            description="The email or password is incorrect.",
            model=schemes.ErrorResponse,
            example={
                "errors": [],
                "message": "The email or password is incorrect",
                "status": status.HTTP_401_UNAUTHORIZED,
            },
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: responses.validation_response(
            example={
                "errors": [
                    {
                        "message": "The email format is invalid",
                        "type": "email",
                    },
                    {
                        "message": "The password length is invalid",
                        "type": "password",
                    },
                ],
                "message": "Validation error",
                "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            },
        ),
    },
)
async def authenticate_user(
    login_user: Annotated[
        schemes.LoginUser,
        Body(),
    ],
    async_session: Annotated[
        AsyncSession,
        Depends(database.get_async_session),
    ],
) -> JSONResponse:
    user: User | None = await crud.get_user_by_email(
        async_session=async_session,
        email=login_user.email,
    )

    if not user or not user.is_password_valid(login_user.password):
        raise HTTPError(
            errors=[],
            message="The email or password is incorrect",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    response: JSONResponse = JSONResponse(
        content=schemes.SuccessResponse(
            message="User authenticated successfully",
            status=status.HTTP_200_OK,
        ).model_dump(mode="json"),
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=jwt.generate_token(
            TokenType.ACCESS,
            user_id=user.id,
            email=user.email,
            key=settings.jwt.JWT_SECRET,
            current_time=utils.now(),
        ),
        max_age=settings.jwt.JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES * 60,
        secure=True,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=jwt.generate_token(
            TokenType.REFRESH,
            user_id=user.id,
            email=user.email,
            key=settings.jwt.JWT_SECRET,
            current_time=utils.now(),
        ),
        max_age=settings.jwt.JWT_REFRESH_TOKEN_EXPIRES_IN_DAYS * 24 * 60 * 60,
        secure=True,
        httponly=True,
    )
    return response


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Refreshes the access token using the refresh token.",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: responses.response(
            description="Tokens refreshed successfully.",
            model=schemes.SuccessResponse,
            example={
                "message": "Tokens refreshed successfully",
                "status": status.HTTP_200_OK,
            },
        ),
        status.HTTP_400_BAD_REQUEST: responses.INVALID_TOKEN,
        status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
        status.HTTP_422_UNPROCESSABLE_ENTITY: responses.INVALID_TOKEN,
    },
)
def refresh_user(
    user: Annotated[
        User,
        Depends(jwt.get_refreshed_user),
    ],
) -> JSONResponse:
    response: JSONResponse = JSONResponse(
        content=schemes.SuccessResponse(
            message="Tokens refreshed successfully",
            status=status.HTTP_200_OK,
        ).model_dump(mode="json"),
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=jwt.generate_token(
            TokenType.ACCESS,
            user_id=user.id,
            email=user.email,
            key=settings.jwt.JWT_SECRET,
            current_time=utils.now(),
        ),
        max_age=settings.jwt.JWT_ACCESS_TOKEN_EXPIRES_IN_MINUTES * 60,
        secure=True,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=jwt.generate_token(
            TokenType.REFRESH,
            user_id=user.id,
            email=user.email,
            key=settings.jwt.JWT_SECRET,
            current_time=utils.now(),
        ),
        max_age=settings.jwt.JWT_REFRESH_TOKEN_EXPIRES_IN_DAYS * 24 * 60 * 60,
        secure=True,
        httponly=True,
    )
    return response
