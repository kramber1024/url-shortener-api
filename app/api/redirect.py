from typing import TYPE_CHECKING, Annotated

from fastapi import APIRouter, Depends, Path, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
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
    url: Url | None = await crud.get_url_by_slug(session=session, slug=slug)

    if url is None:
        # TODO @kramber: Redirect to real 404 page
        # 001

        return RedirectResponse(url="/404")

    await crud.create_click(
        session=session,
        url_id=url.id,
        ip=request.client.host if request.client else "None",
        country="None",
    )
    await crud.update_url(session=session, url=url, total_clicks=url.total_clicks + 1)

    return RedirectResponse(url=url.address, status_code=301)