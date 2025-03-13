from app.core.database.models.mixins import TableNameMixin


def test_table_name_mixin_property_tablename_without_s() -> None:
    class User(TableNameMixin): ...

    user: User = User()

    assert user.__tablename__ == "Users"


def test_table_name_mixin_property_tablename_with_s() -> None:
    class Status(TableNameMixin): ...

    status: Status = Status()

    assert status.__tablename__ == "Statuses"
