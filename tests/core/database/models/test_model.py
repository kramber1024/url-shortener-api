from app.core.database.models import Model


def test_model_attribute_abstract() -> None:
    assert Model.__abstract__ is True
