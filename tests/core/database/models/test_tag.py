import pytest

from app.core.database.models import Tag
from app.core.settings.data import Name


@pytest.fixture(scope="module")
def url_id() -> int:
    return 1


@pytest.fixture(scope="module")
def name() -> str:
    return "tag"


@pytest.fixture(scope="module")
def tag(url_id: int, name: str) -> Tag:
    return Tag(url_id=url_id, name=name)


@pytest.mark.parametrize(
    "name",
    [
        "a" * (Name.MIN_LENGTH - 1),
        "a" * (Name.MAX_LENGTH + 1),
    ],
)
def test_tag_init_invalid_name(url_id: int, name: str) -> None:
    with pytest.raises(ValueError, match=r"^$"):
        Tag(url_id=url_id, name=name)


def test_tag_init(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name=name)

    assert hasattr(tag, "id")
    assert tag.url_id == url_id
    assert tag.name == name
    assert hasattr(tag, "created_at")


def test_tag_url_id_property(url_id: int, name: str) -> None:
    tag: Tag = Tag(url_id=url_id, name=name)

    assert tag.url_id == url_id


def test_tag_name_property(tag: Tag, name: str) -> None:
    assert tag.name == name


def test_tag_name_property_setter_invalid(tag: Tag) -> None:
    with pytest.raises(ValueError, match=r"^$"):
        tag.name = ""


def test_tag_name_property_setter(tag: Tag) -> None:
    new_name: str = "name"

    tag.name = new_name

    assert tag.name == new_name


def test_tag_repr(tag: Tag) -> None:
    assert repr(tag) == f"<Tag {tag.name}>"
