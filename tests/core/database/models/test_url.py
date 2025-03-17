import pytest

from app.core.database.models import Url
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


@pytest.fixture()
def url() -> Url:
    return Url(user_id=1, source="https://example.com", slug="example")


@pytest.mark.parametrize("user_id", [0, 1, 2])
@pytest.mark.parametrize(
    "source",
    ["https://a.b", "http://example.com", "https://another.com"],
)
@pytest.mark.parametrize(
    "slug",
    ["example", "a" * Slug.MAX_LENGTH, "a" * Slug.MIN_LENGTH, "another"],
)
def test_url_init(user_id: int, source: str, slug: str) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    assert url._user_id == user_id
    assert url.source == source
    assert url.slug == slug
    assert url.total_clicks == 0


@pytest.mark.parametrize("user_id", [0, 1, 2])
def test_url_property_user_id(user_id: int, source: str, slug: str) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    assert url.user_id == user_id


@pytest.mark.parametrize(
    "source",
    [
        "https://example.com",
        "https://test.com",
        "https://another.com",
        "a" * Source.MAX_LENGTH,
        "a" * Source.MIN_LENGTH,
    ],
)
def test_url_property_source(user_id: int, source: str, slug: str) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    assert url.source == source


@pytest.mark.parametrize(
    "source",
    ["https://example.com", "https://test.com", "https://another.com"],
)
def test_url_property_source_setter(source: str, url: Url) -> None:
    url.source = source

    assert url.source == source


@pytest.mark.parametrize(
    "source",
    ["", "a" * (Source.MAX_LENGTH + 1), "a" * (Source.MIN_LENGTH - 1)],
)
def test_url_property_source_setter_invalid_length(
    source: str,
    url: Url,
) -> None:
    with pytest.raises(ValueError, match=".*"):
        url.source = source


@pytest.mark.parametrize(
    "slug",
    [
        "example",
        "test",
        "a" * Slug.MAX_LENGTH,
        "a" * Slug.MIN_LENGTH,
    ],
)
def test_url_property_slug(user_id: int, source: str, slug: str) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)

    assert url.slug == slug


@pytest.mark.parametrize("slug", ["example", "test", "another"])
def test_url_property_slug_setter(slug: str, url: Url) -> None:
    url.slug = slug

    assert url.slug == slug


@pytest.mark.parametrize(
    "slug",
    ["", "a" * (Slug.MAX_LENGTH + 1), "a" * (Slug.MIN_LENGTH - 1)],
)
def test_url_property_slug_setter_invalid_length(slug: str, url: Url) -> None:
    with pytest.raises(ValueError, match=".*"):
        url.slug = slug


@pytest.mark.parametrize("total_clicks", [0, 1, 100])
def test_url_property_total_clicks(
    user_id: int,
    source: str,
    slug: str,
    total_clicks: int,
) -> None:
    url: Url = Url(user_id=user_id, source=source, slug=slug)
    url.total_clicks = total_clicks

    assert url.total_clicks == total_clicks


@pytest.mark.parametrize("total_clicks", [0, 1, 100])
def test_url_property_total_clicks_setter(url: Url, total_clicks: int) -> None:
    url.total_clicks = total_clicks

    assert url.total_clicks == total_clicks


@pytest.mark.parametrize("total_clicks", [-1, -100])
def test_url_property_total_clicks_setter_invalid_value(
    url: Url,
    total_clicks: int,
) -> None:
    with pytest.raises(ValueError, match=".*"):
        url.total_clicks = total_clicks


def test_url_repr(url: Url) -> None:
    assert repr(url) == f"<Url /{url.slug} -> {url.source}>"
