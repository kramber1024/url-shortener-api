from fastapi import APIRouter

redirector: APIRouter = APIRouter(prefix="", include_in_schema=False)

__all__ = ("redirector",)
