import pytest

from app.core.database.models import Tag
from app.core.settings.data import Name


@pytest.fixture(scope="module")
def url_id() -> int:
    return 1


@pytest.fixture(scope="module")
def name() -> str:
    return "name"


@pytest.fixture()
def tag() -> Tag:
    return Tag(url_id=1, name="name")


@pytest.mark.parametrize("url_id", [0, 1, 2])
@pytest.mark.parametrize("name", ["somename", "AnotherName", "$@#%$^&*_(){[]}"])
def test_tag_init(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name=name)

    assert tag._url_id == url_id
    assert tag.name == name


@pytest.mark.parametrize("url_id", [0, 1, 2])
def test_tag_property_url_id(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name=name)

    assert tag.url_id == url_id


@pytest.mark.parametrize(
    "name",
    ["somename", "AnotherName", "a" * Name.MAX_LENGTH, "a" * Name.MIN_LENGTH],
)
def test_tag_property_name(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name=name)

    assert tag.name == name


@pytest.mark.parametrize("name", ["SomeName", "AnotherName", "$@#%$^&*"])
def test_tag_property_name_setter(name: str, tag: Tag) -> None:
    tag.name = name

    assert tag.name == name


@pytest.mark.parametrize(
    "name",
    ["", "a" * (Name.MAX_LENGTH + 1), "a" * (Name.MIN_LENGTH - 1)],
)
def test_tag_property_name_setter_invalid_length(name: str, tag: Tag) -> None:
    with pytest.raises(ValueError, match="^$"):
        tag.name = name


def test_tag_repr(tag: Tag) -> None:
    assert repr(tag) == f"<Tag {tag.name}>"
