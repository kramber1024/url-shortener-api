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
        status.HTTP_200_OK: responses.response(
            description="User information retrieved successfully.",
            model=schemes.User,
            example={
                "email": "email@domain.tld",
                "first_name": "John",
                "last_name": "Doe",
                "id": "7250096872525709312",
            },
        ),
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


@router.get("/me/urls", summary="Get all")
async def get_users_me_urls(
    user: Annotated[
        User,
        Depends(jwt_.get_current_user),
    ],
) -> JSONResponse:
    return JSONResponse(
        content=schemes.UrlList.from_model(user.urls).model_dump(),
        status_code=status.HTTP_200_OK,
    )
