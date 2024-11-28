from fastapi import APIRouter

from .controller import router

redirector: APIRouter = APIRouter(prefix="", include_in_schema=False)
redirector.include_router(router)

__all__ = ("redirector",)
