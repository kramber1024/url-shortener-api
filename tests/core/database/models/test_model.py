from app.core.database.models import Model


def test_model_attribute___abstract__() -> None:
    assert hasattr(Model, "__abstract__")
    assert Model.__abstract__ is True
