import pytest

from app.core.database.models.url import Url
from app.core.settings.data import Slug, Source


@pytest.fixture(scope="module")
def user_id() -> int:
    return 1


@pytest.fixture(scope="module")
def source() -> str:
    return "https://example.com"


@pytest.fixture(scope="module")
def slug() -> str:
    return "example"


def test_url_init(user_id: int, source: str, slug: str) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    assert url.user_id == user_id
    assert url.source == source
    assert url.slug == slug
    assert url.total_clicks == 0


@pytest.mark.parametrize("user_id", [123, 456, 789, -1, 0])
def test_url_property_user_id(user_id: int, source: str, slug: str) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    assert url.user_id == user_id


@pytest.mark.parametrize(
    "source",
    [
        "https://example.com",
        "http://example.com",
        "https://sub.example.com/path?query=param",
        "http://a.b",
        "https://aadadda.k",
    ],
)
def test_url_property_source(user_id: int, source: str, slug: str) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    assert url.source == source


@pytest.mark.parametrize(
    "source",
    [
        "a" * (Source.MAX_LENGTH + 1),
        "a" * (Source.MAX_LENGTH + 100),
        "a" * (Source.MIN_LENGTH - 1),
        "a" * (Source.MIN_LENGTH - 100),
        "",
    ],
)
def test_url_property_source_invalid_length(
    user_id: int,
    source: str,
    slug: str,
) -> None:
    url: Url = Url(user_id=user_id, source="a" * Source.MAX_LENGTH, slug=slug)

    with pytest.raises(ValueError, match="^$"):
        url.source = source


@pytest.mark.parametrize(
    "source",
    [
        "https://example.com",
        "http://example.com",
        "https://sub.example.com/path?query=param",
        "http://a.b",
        "https://aadadda.k",
    ],
)
def test_url_property_source_valid_length(
    user_id: int,
    source: str,
    slug: str,
) -> None:
    url: Url = Url(user_id=user_id, source="a" * Source.MIN_LENGTH, slug=slug)

    url.source = source

    assert url.source == source


@pytest.mark.parametrize(
    "slug",
    [
        "example",
        "ex",
        "slug-example",
        "slug_example",
    ],
)
def test_url_property_slug(user_id: int, source: str, slug: str) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    assert url.slug == slug


@pytest.mark.parametrize(
    "slug",
    [
        "a" * (Slug.MAX_LENGTH + 1),
        "a" * (Slug.MAX_LENGTH + 100),
        "a" * (Slug.MAX_LENGTH + 1000),
        "a" * (Slug.MIN_LENGTH - 1),
        "",
    ],
)
def test_url_property_slug_invalid_length(
    user_id: int,
    source: str,
    slug: str,
) -> None:
    url = Url(user_id=user_id, source=source, slug="a" * Slug.MAX_LENGTH)

    with pytest.raises(ValueError, match="^$"):
        url.slug = slug


@pytest.mark.parametrize(
    "slug",
    [
        "a" * Slug.MIN_LENGTH,
        "e" * Slug.MAX_LENGTH,
        "slug-example",
        "slug_example",
        "short",
    ],
)
def test_url_property_slug_valid_length(
    user_id: int,
    source: str,
    slug: str,
) -> None:
    url: Url = Url(user_id=user_id, source=source, slug="u" * Slug.MAX_LENGTH)

    url.slug = slug

    assert url.slug == slug


@pytest.mark.parametrize("total_clicks", [0, 1, 100, 1000])
def test_url_property_total_clicks(
    user_id: int,
    source: str,
    slug: str,
    total_clicks: int,
) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)
    url.total_clicks = total_clicks

    assert url.total_clicks == total_clicks


@pytest.mark.parametrize("total_clicks", [-1, -100])
def test_url_property_total_clicks_invalid(
    user_id: int,
    source: str,
    slug: str,
    total_clicks: int,
) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    with pytest.raises(ValueError, match="^$"):
        url.total_clicks = total_clicks


@pytest.mark.parametrize("total_clicks", [0, 1, 100, 1000])
def test_url_property_total_clicks_valid(
    user_id: int,
    source: str,
    slug: str,
    total_clicks: int,
) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    url.total_clicks = total_clicks

    assert url.total_clicks == total_clicks


def test_url_repr(user_id: int, source: str, slug: str) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    assert repr(url) == f"<Url /{slug} -> {source}>"
