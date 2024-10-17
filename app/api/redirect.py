from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, Path, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.exceptions import HTTPError
from app.core import utils
from app.core.config import settings
from app.core.database import db

if TYPE_CHECKING:
    from app.core.database.models import Url

redirect: APIRouter = APIRouter(prefix="", include_in_schema=False)


@redirect.get("/{slug}", response_class=RedirectResponse)
async def redirect_to_url(
    request: Request,
    slug: Annotated[str, Path()],
    session: Annotated[
        AsyncSession,
        Depends(db.scoped_session),
    ],
) -> RedirectResponse:
    if slug == settings.data.NOT_FOUND_PAGE_URL:
        raise HTTPError(
            errors=[],
            message="Not Found",
            status=status.HTTP_404_NOT_FOUND,
        )

    url: Url | None = await crud.get_url_by_slug(session=session, slug=slug)

    if url is None:
        return RedirectResponse(
            url=settings.data.NOT_FOUND_PAGE_URL,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    ip: str | None = request.client.host if request.client else None
    country: str | None = None
    if ip:
        country = await utils.get_country_by_ip(
            session=session,
            ip=ip,
        )

    await crud.create_click(
        session=session,
        url_id=url.id,
        ip=ip,
        country=country,
    )
    await crud.update_url(session=session, url=url, total_clicks=url.total_clicks + 1)

    return RedirectResponse(url=url.address, status_code=307)
