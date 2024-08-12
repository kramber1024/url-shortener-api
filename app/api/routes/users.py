from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.api import responses, schemes
from app.core.auth import jwt_
from app.core.database.models import User

router: APIRouter = APIRouter(
    prefix="/users",
    responses={
        status.HTTP_400_BAD_REQUEST: responses.INVALID_TOKEN,
        status.HTTP_401_UNAUTHORIZED: responses.UNAUTHORIZED,
    },
)


@router.get(
    "/me",
    summary="Get current user",
    description="Get information about the current user",
    responses={
        200: {
            "description": "User information retrieved successfully.",
            "model": schemes.User,
            "content": {
                "application/json": {
                    "example": {
                        "id": "7207306656936357888",
                        "name": "kramber",
                        "email": "email@domain.tld",
                    },
                },
            },
        },
    },
)
def get_users_me(
    user: Annotated[
        User,
        Depends(jwt_.get_current_user),
    ],
) -> JSONResponse:
    return JSONResponse(
        content=schemes.User.from_model(user).model_dump(),
        status_code=status.HTTP_200_OK,
    )
