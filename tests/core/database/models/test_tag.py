import pytest

from app.core.database.models import Tag
from app.core.settings.data import Name


@pytest.fixture(scope="module")
def url_id() -> int:
    return 1


@pytest.fixture(scope="module")
def name() -> str:
    return "name"


def test_tag_init(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name=name)

    assert tag.url_id == url_id
    assert tag.name == name


@pytest.mark.parametrize("url_id", [123321, 77850370187, 14991194284, -1, 0])
def test_tag_property_url_id(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name=name)

    assert tag.url_id == url_id


@pytest.mark.parametrize(
    "name",
    [
        "t" * Name.MIN_LENGTH,
        "t" * Name.MAX_LENGTH,
        "name",
        "tag-name",
        "tag_name",
    ],
)
def test_tag_property_name(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name=name)

    assert tag.name == name


@pytest.mark.parametrize(
    "name",
    [
        "t" * (Name.MIN_LENGTH - 1),
        "t" * (Name.MAX_LENGTH + 1),
        "t" * (Name.MAX_LENGTH + 100),
        "t" * (Name.MAX_LENGTH + 1000),
        "t" * (Name.MAX_LENGTH + 10000),
    ],
)
def test_tag_property_name_invalid_length(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name="t" * Name.MIN_LENGTH)

    with pytest.raises(ValueError, match="^$"):
        tag.name = name


@pytest.mark.parametrize(
    "name",
    [
        "t" * Name.MIN_LENGTH,
        "t" * Name.MAX_LENGTH,
        "name",
        "tag-name",
        "tag_name",
    ],
)
def test_tag_property_name_valid_length(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name="t" * Name.MIN_LENGTH)

    tag.name = name

    assert tag.name == name


def test_tag_repr(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name=name)

    assert repr(tag) == f"<Tag {name}>"
