from fastapi import APIRouter

from .routes import auth, users
from .schemes import ErrorResponse as ErrorResponseScheme

api: APIRouter = APIRouter(
    prefix="/api",
    responses={
        500: {
            "description": "Something went very wrong. Please report this issue.",
            "model": ErrorResponseScheme,
            "content": {
                "application/json": {
                    "example": {
                        "errors": [],
                        "message": "Internal server error",
                        "status": 500,
                    },
                },
            },
        },
    },
)
api.include_router(users.router, tags=["Users"])
api.include_router(auth.router, tags=["Auth"])
