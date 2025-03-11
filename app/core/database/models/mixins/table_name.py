from sqlalchemy.ext.declarative import declared_attr


class TableNameMixin:
    """Mixin for setting the name of a table in a database.

    Automatically sets the name of a table to the name of a class in the plural
    form.
    """

    @declared_attr.directive
    def __tablename__(self) -> str:
        """The name of the table in the database.

        Raises:
            AttributeError: If the class does not have a __name__ attribute.
        """
        if not hasattr(self, "__name__") or not isinstance(self.__name__, str):
            raise AttributeError

        table_name: str = self.__name__

        if table_name.endswith("s"):
            return table_name + "es"

        return table_name + "s"
