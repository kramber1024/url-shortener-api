"""Main module for the FastAPI application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.api import api
from app.api.handlers import (
    exception_handler,
    http_exception_handler,
    request_validation_error_handler,
)
from app.core.database import database
from app.core.settings import settings
from app.redirector import redirector


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    await database.create_tables(hard_reset=False)
    yield
    await database.shutdown()


app: FastAPI = FastAPI(
    title=f"{settings.app.NAME} - API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan,
    root_path_in_servers=False,
)
app.include_router(api)
app.include_router(redirector)
app.add_exception_handler(
    RequestValidationError,
    request_validation_error_handler,  # type: ignore[arg-type]
)
app.add_exception_handler(
    HTTPException,
    http_exception_handler,  # type: ignore[arg-type]
)
app.add_exception_handler(
    Exception,
    exception_handler,
)


if __name__ == "__main__":
    uvicorn.run(
        "app.__main__:app",
        host=settings.development.HOST,
        port=settings.development.PORT,
        reload=True,
    )
