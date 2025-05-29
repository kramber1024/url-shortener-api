"""CRUD operations.

This module provides functions to interact with the database.
"""

from .click import create_click
from .network import get_network_by_ip
from .status import create_status
from .tag import create_tag
from .url import create_url, get_url_by_slug, update_url
from .user import create_user, get_user_by_email, get_user_by_id

__all__ = [
    "create_click",
    "create_status",
    "create_tag",
    "create_url",
    "create_user",
    "get_network_by_ip",
    "get_url_by_slug",
    "get_user_by_email",
    "get_user_by_id",
    "update_url",
]
