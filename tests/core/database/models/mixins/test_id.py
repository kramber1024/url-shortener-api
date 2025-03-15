from app.core.database.models.mixins import IdMixin


def test_id_mixin_property_id() -> None:
    assert IdMixin.id
