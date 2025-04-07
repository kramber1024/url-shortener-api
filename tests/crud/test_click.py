from typing import TYPE_CHECKING

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database.models import Click

if TYPE_CHECKING:
    from sqlalchemy import Result


@pytest.fixture(scope="module")
def url_id() -> int:
    return 1


@pytest.fixture(scope="module")
def ip() -> str:
    return "127.0.0.1"


@pytest.fixture(scope="module")
def country() -> str:
    return "es"


@pytest.mark.asyncio()
async def test_create_click(
    async_session: AsyncSession,
    url_id: int,
    ip: str,
    country: str,
) -> None:
    click: Click = await crud.create_click(
        async_session=async_session,
        url_id=url_id,
        ip=ip,
        country=country,
    )

    result: Result[tuple[Click]] = await async_session.execute(
        select(Click).where(Click.id == click.id),
    )
    database_click: Click | None = result.scalars().first()
    assert database_click
    assert database_click.id == click.id
    assert database_click.url_id == click.url_id
    assert database_click.ip == click.ip
    assert database_click.country == click.country
