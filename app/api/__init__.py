from fastapi import APIRouter, status

from app.api import responses
from app.api.routes import auth, urls, users

api: APIRouter = APIRouter(
    prefix="/api",
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: responses.INTERNAL_SERVER_ERROR,
    },
)
api.include_router(users.router, tags=["Users"])
api.include_router(auth.router, tags=["Auth"])
api.include_router(urls.router, tags=["Urls"])

__all__: tuple[str, ...] = ("api",)
