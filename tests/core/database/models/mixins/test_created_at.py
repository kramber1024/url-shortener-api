from app.core.database.models.mixins import CreatedAtMixin


def test_created_at_mixin_attribute__created_at() -> None:
    assert hasattr(CreatedAtMixin, "_created_at")


def test_created_at_mixin_property_created_at() -> None:
    assert CreatedAtMixin.created_at
