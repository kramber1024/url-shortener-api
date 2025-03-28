from typing import TYPE_CHECKING

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database.models import Tag

if TYPE_CHECKING:
    from sqlalchemy import Result


@pytest.fixture(scope="module")
def url_id() -> int:
    return 1


@pytest.fixture(scope="module")
def name() -> str:
    return "name"


@pytest.mark.asyncio()
async def test_create_tag(
    async_session: AsyncSession,
    url_id: int,
    name: str,
) -> None:
    tag: Tag = await crud.create_tag(
        async_session=async_session,
        url_id=url_id,
        name=name,
    )

    result: Result[tuple[Tag]] = await async_session.execute(
        select(Tag).where(Tag.id == tag.id),
    )
    database_tag: Tag | None = result.scalars().first()

    assert database_tag
    assert database_tag.id == tag.id
    assert database_tag.url_id == url_id
    assert database_tag.name == name
