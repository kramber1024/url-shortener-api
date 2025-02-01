"""Module for database model mixins."""

from .created_at import CreatedAtMixin
from .id import IdMixin
from .tablename import TableNameMixin
from .updated_at import UpdatedAtMixin

__all__ = ["CreatedAtMixin", "IdMixin", "TableNameMixin", "UpdatedAtMixin"]
