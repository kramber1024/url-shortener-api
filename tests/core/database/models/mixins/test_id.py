from app.core.database.models.mixins import IdMixin


def test_id_mixin_attribute__id() -> None:
    assert hasattr(IdMixin, "_id")


def test_id_mixin_property_id() -> None:
    assert IdMixin.id
