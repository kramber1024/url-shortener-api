import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api import api
from app.api.exceptions import ErrorException
from app.api.handlers import (
    error_exception_handler,
    server_error_exception_handler,
    validation_exception_handler,
)
from app.core.config import settings
from app.core.database import db

app: FastAPI = FastAPI(
    title=f"{settings.app.NAME} API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    root_path_in_servers=False,
)
app.include_router(api)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ErrorException, error_exception_handler)
app.add_exception_handler(Exception, server_error_exception_handler)


async def main() -> None:
    await db.create_db(hard_rest=False)

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=26800,
        reload=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
