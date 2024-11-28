from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, Path, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.api.exceptions import HTTPError
from app.core import utils
from app.core.database import database
from app.core.settings.data import Page

if TYPE_CHECKING:
    from app.core.database.models import Url

router: APIRouter = APIRouter(prefix="")


@router.get("/{slug}", response_class=RedirectResponse)
async def redirect_to_url(
    request: Request,
    slug: Annotated[
        str,
        Path(),
    ],
    async_session: Annotated[
        AsyncSession,
        Depends(database.get_async_session),
    ],
) -> RedirectResponse:
    if slug == Page.NOT_FOUND:
        raise HTTPError(
            errors=[],
            message="Not Found",
            status=status.HTTP_404_NOT_FOUND,
        )

    url: Url | None = await crud.get_url_by_slug(
        async_session=async_session,
        slug=slug,
    )

    if not url:
        return RedirectResponse(
            url=Page.NOT_FOUND.value,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )

    ip: str | None = request.client.host if request.client else None
    country: str | None = None
    if ip:
        country = await utils.get_country_by_ip(
            session=async_session,
            ip=ip,
        )

    await crud.create_click(
        async_session=async_session,
        url_id=url.id,
        ip=ip,
        country=country,
    )
    await crud.update_url(
        async_session=async_session,
        url=url,
        total_clicks=url.total_clicks + 1,
    )

    return RedirectResponse(
        url=url.address,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
