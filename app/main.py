import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api import api
from app.api.exceptions import HTTPError
from app.api.handlers import (
    exception_handler,
    http_error_handler,
    request_validation_error_handler,
)
from app.core.config import settings
from app.core.database import db
from app.redirector import redirector

app: FastAPI = FastAPI(
    title=f"{settings.app.NAME} - API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    root_path_in_servers=False,
)
app.include_router(api)
app.include_router(redirector)
app.add_exception_handler(
    RequestValidationError,
    request_validation_error_handler,  # type: ignore[arg-type]
)
app.add_exception_handler(
    HTTPError,
    http_error_handler,  # type: ignore[arg-type]
)
app.add_exception_handler(
    Exception,
    exception_handler,
)


async def main() -> None:
    await db.create_db(hard_rest=False)

    uvicorn.run(
        "app.main:app",
        host=settings.dev.HOST,
        port=settings.dev.PORT,
        reload=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
