"""Module for data constraints.

This module provides various data constraints for the application. Each
constraint is defined as an ` Enum ` class.
"""

from .address import Address
from .country import Country
from .first_name import FirstName
from .last_name import LastName
from .mail import Email
from .mask import Mask
from .name import Name
from .page import Page
from .password import Password
from .phone import Phone
from .slug import Slug
from .source import Source
from .user import User

__all__ = [
    "Address",
    "Country",
    "Email",
    "FirstName",
    "LastName",
    "Mask",
    "Name",
    "Page",
    "Password",
    "Phone",
    "Slug",
    "Source",
    "User",
]
