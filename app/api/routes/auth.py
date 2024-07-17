from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.exceptions import ErrorException
from app.api.schemes import ErrorResponse as ErrorResponseScheme
from app.api.schemes import SuccessResponse as SuccessResponseScheme
from app.api.schemes import UserLogin as UserLoginScheme
from app.api.schemes import UserRegistration as UserRegistrationScheme
from app.core.auth import jwt_auth
from app.core.config import settings
from app.core.database import db
from app.core.database.models import User

router: APIRouter = APIRouter(prefix="/auth")


@router.post(
    "/register",
    summary="Create a new user account",
    description="Registers new user account in the system.",
    status_code=201,
    responses={
        201: {
            "description": "New user account registered successfully.",
            "model": SuccessResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "message": "Account created successfully",
                        "status": 201,
                    },
                },
            },
        },
        409: {
            "description": (
                "The email is already in use. "
                "User should use a different email or login."
            ),
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "The email is already in use",
                        "status": 409,
                    },
                },
            },
        },
        422: {
            "description": (
                "Validation error. "
                "The email format is invalid and/or the password length is incorrect "
                "(either too short or too long). Same goes for name fields. "
                "Also you can get this error if "
                "you forgot to fill in the required fields."
            ),
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
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
                        "status": 422,
                    },
                },
            },
        },
    },
)
async def register_user(
    new_user: Annotated[
        UserRegistrationScheme,
        Body(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
    ],
) -> JSONResponse:

    if await crud.get_user_by_email(
        session=session,
        email=new_user.email,
    ) is not None:
        raise ErrorException(
            errors=[],
            message="The email is already in use",
            status=status.HTTP_409_CONFLICT,
        )

    user: User = await crud.create_user(
        session=session,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        password=new_user.password,
    )
    await crud.create_status(
        session=session,
        user_id=user.id,
        active=True,
        premium=False,
    )

    success_response: SuccessResponseScheme = SuccessResponseScheme(
        message="Account created successfully",
        status=status.HTTP_201_CREATED,
    )

    return JSONResponse(
        content=success_response.model_dump(),
        status_code=status.HTTP_201_CREATED,
    )


@router.post(
    "/login",
    summary="Authenticate user",
    description="Authenticates a user in the system using email and password.",
    status_code=200,
    responses={
        200: {
            "description": "User authenticated successfully.",
            "model": SuccessResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "message": "User authenticated successfully",
                        "status": 200,
                    },
                },
            },
        },
        401: {
            "description": "The email or password is incorrect.",
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "The email or password is incorrect",
                        "status": 401,
                    },
                },
            },
        },
        422: {
            "description": (
                "Validation error. "
                "The email format is invalid and/or the password length is incorrect "
                "(either too short or too long). "
                "Also you can get this error if "
                "you forgot to fill in the required fields."
            ),
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
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
                        "status": 422,
                    },
                },
            },
        },
    },
)
async def authenticate_user(
    user_login: Annotated[
        UserLoginScheme,
        Body(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
    ],
) -> JSONResponse:

    user: User | None = await crud.get_user_by_email(
        session=session,
        email=user_login.email,
    )

    if user is None or not user.is_password_valid(user_login.password):
        raise ErrorException(
            errors=[],
            message="The email or password is incorrect",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    success_response: SuccessResponseScheme = SuccessResponseScheme(
        message="User authenticated successfully",
        status=status.HTTP_200_OK,
    )

    response: JSONResponse = JSONResponse(
        content=success_response.model_dump(),
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=jwt_auth.generate_access_token(user.id, user.email),
        max_age=settings.jwt.ACCESS_TOKEN_EXPIRES_MINUTES * 60,
        secure=True,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=jwt_auth.generate_refresh_token(user.id, user.email),
        max_age=settings.jwt.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 60,
        secure=True,
        httponly=True,
    )

    return response


@router.post(
    "/refresh",
    summary="Refresh access token",
    description="Refreshes the access token using the refresh token.",
    status_code=200,
    responses={
        200: {
            "description": "Tokens refreshed successfully.",
            "model": SuccessResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "message": "Tokens refreshed successfully",
                        "status": 200,
                    },
                },
            },
        },
        400: {
            "description": "Provided token is not valid.",
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "Invalid token",
                        "status": 400,
                    },
                },
            },
        },
        401: {
            "description": "Authorization required. Provide a valid token in headers.",
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "Authorization required",
                        "status": 401,
                    },
                },
            },
        },
        422: {
            "description": "Provided token is not valid.",
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "Invalid token",
                        "status": 400,
                    },
                },
            },
        },
    },
)
def refresh_user(
    user: Annotated[
        User,
        Depends(jwt_auth.get_refreshed_user),
    ],
) -> JSONResponse:

    success_response: SuccessResponseScheme = SuccessResponseScheme(
        message="Tokens refreshed successfully",
        status=status.HTTP_200_OK,
    )

    response: JSONResponse = JSONResponse(
        content=success_response.model_dump(),
        status_code=status.HTTP_200_OK,
    )
    response.set_cookie(
        key="access_token",
        value=jwt_auth.generate_access_token(user.id, user.email),
        max_age=settings.jwt.ACCESS_TOKEN_EXPIRES_MINUTES * 60,
        secure=True,
        httponly=True,
    )
    response.set_cookie(
        key="refresh_token",
        value=jwt_auth.generate_refresh_token(user.id, user.email),
        max_age=settings.jwt.REFRESH_TOKEN_EXPIRES_DAYS * 24 * 60 * 60,
        secure=True,
        httponly=True,
    )

    return response
