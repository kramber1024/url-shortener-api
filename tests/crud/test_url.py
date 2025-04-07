import pytest
import pytest_asyncio
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.database.models import Url


@pytest.fixture(scope="module")
def user_id() -> int:
    return 1


@pytest.fixture(scope="module")
def source() -> str:
    return "https://example.com"


@pytest.fixture(scope="module")
def slug() -> str:
    return "example"


@pytest_asyncio.fixture()
async def url(async_session: AsyncSession) -> Url:
    url: Url = Url(user_id=1, source="https://example.com", slug="example")

    async_session.add(url)
    await async_session.commit()

    return url


@pytest.mark.asyncio()
async def test_create_url(
    async_session: AsyncSession,
    user_id: int,
    source: str,
    slug: str,
) -> None:
    url: Url = await crud.create_url(
        async_session=async_session,
        user_id=user_id,
        source=source,
        slug=slug,
    )

    result: Result[tuple[Url]] = await async_session.execute(
        select(Url).where(Url.user_id == user_id),
    )
    database_url: Url | None = result.scalars().first()
    assert database_url
    assert database_url.user_id == url.user_id
    assert database_url.source == url.source
    assert database_url.slug == url.slug


@pytest.mark.asyncio()
async def test_get_url_by_slug(
    async_session: AsyncSession,
    url: Url,
) -> None:
    database_url: Url | None = await crud.get_url_by_slug(
        async_session=async_session,
        slug=url.slug,
    )

    assert database_url is not None
    assert database_url.slug == url.slug


@pytest.mark.asyncio()
async def test_get_url_by_slug_not_found(
    async_session: AsyncSession,
    url: Url,
) -> None:
    database_url: Url | None = await crud.get_url_by_slug(
        async_session=async_session,
        slug=url.slug[::-1],
    )

    assert database_url is None


@pytest.mark.asyncio()
async def test_update_url(async_session: AsyncSession, url: Url) -> None:
    updated_source: str = url.source[::-1]
    updated_slug: str = url.slug[::-1]
    updated_total_clicks: int = url.total_clicks + 1

    await crud.update_url(
        async_session=async_session,
        url=url,
        source=updated_source,
        slug=updated_slug,
        total_clicks=updated_total_clicks,
    )

    result: Result[tuple[Url]] = await async_session.execute(
        select(Url).where(Url.user_id == url.user_id),
    )
    database_url: Url | None = result.scalars().first()
    assert database_url
    assert database_url.source == updated_source
    assert database_url.slug == updated_slug
    assert database_url.total_clicks == updated_total_clicks
