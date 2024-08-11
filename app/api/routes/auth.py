from typing import Annotated

from fastapi import APIRouter, Body, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api import responses, schemes
from app.api.exceptions import HTTPError
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
        status.HTTP_201_CREATED: responses.response(
            description="New user account registered successfully.",
            model=schemes.SuccessResponse,
            example={
                "message": "Account created successfully",
                "status": 201,
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
                "status": 409,
            },
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: responses.validation_error_response(
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
                "status": 422,
            },
        ),
    },
)
async def register_user(
    new_user: Annotated[
        schemes.UserRegistration,
        Body(),
    ],
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
    ],
) -> JSONResponse:
    if (
        await crud.get_user_by_email(
            session=session,
            email=new_user.email,
        )
        is not None
    ):
        raise HTTPError(
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

    success_response: schemes.SuccessResponse = schemes.SuccessResponse(
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
        status.HTTP_200_OK: responses.response(
            description="User authenticated successfully.",
            model=schemes.SuccessResponse,
            example={
                "message": "User authenticated successfully",
                "status": 200,
            },
        ),
        status.HTTP_401_UNAUTHORIZED: responses.response(
            description="The email or password is incorrect.",
            model=schemes.ErrorResponse,
            example={
                "errors": [],
                "message": "The email or password is incorrect",
                "status": 401,
            },
        ),
        status.HTTP_422_UNPROCESSABLE_ENTITY: responses.validation_error_response(
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
                "status": 422,
            },
        ),
    },
)
async def authenticate_user(
    user_login: Annotated[
        schemes.UserLogin,
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
        raise HTTPError(
            errors=[],
            message="The email or password is incorrect",
            status=status.HTTP_401_UNAUTHORIZED,
        )

    success_response: schemes.SuccessResponse = schemes.SuccessResponse(
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
        status.HTTP_200_OK: responses.response(
            description="Tokens refreshed successfully.",
            model=schemes.SuccessResponse,
            example={
                "message": "Tokens refreshed successfully",
                "status": 200,
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
        Depends(jwt_auth.get_refreshed_user),
    ],
) -> JSONResponse:
    success_response: schemes.SuccessResponse = schemes.SuccessResponse(
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
