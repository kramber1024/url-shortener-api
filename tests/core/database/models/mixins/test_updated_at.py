from app.core.database.models.mixins import UpdatedAtMixin


def test_updated_at_mixin_property_updated_at() -> None:
    assert UpdatedAtMixin.updated_at
