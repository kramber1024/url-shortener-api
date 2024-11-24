from sqlalchemy.ext.declarative import declared_attr


class TableNameMixin:
    """A mixin for setting the table name in the database."""

    @declared_attr.directive
    def __tablename__(self) -> str:
        """The name of the table in the database.

        Raises:
            AttributeError: If the class does not have a __name__ attribute.

        Returns:
            str: The name of the table in the database.
        """
        if not hasattr(self, "__name__") or not isinstance(self.__name__, str):
            raise AttributeError

        table_name: str = self.__name__

        if table_name[-1] == "s":
            return table_name + "es"

        return table_name + "s"
