from typing import Annotated

from pydantic import EmailStr, Field

HTTPStatus = Annotated[
    int,
    Field(
        description="HTTP status code.",
        examples=[422],
        ge=100,
        le=599,
    ),
]

Id = Annotated[
    str,
    Field(
        description="Unique identifier.",
        examples=["7205649978688008192"],
        max_length=len("7205649978688008192"),
        min_length=len("7205649978688008192"),
    ),
]

Email = Annotated[
    EmailStr,
    Field(
        min_length=len("*@*.*"),
        max_length=64,
        description="Email used for authentication and notifications.",
        examples=["email@domain.tld"],
    ),
]

Password = Annotated[
    str,
    Field(
        min_length=8,
        max_length=256,
        description="Used for authentication.",
        examples=["My$uper$ecretPa$$word"],
    ),
]

FirstName = Annotated[
    str,
    Field(
        min_length=3,
        max_length=16,
        description="Used in full name and official emails",
        examples=["John"],
    ),
]

LastName = Annotated[
    str,
    Field(
        min_length=3,
        max_length=16,
        description="Used in full name.",
        examples=["Doe"],
    ),
]

__all__ = (
    "Email",
    "FirstName",
    "HTTPStatus",
    "Id",
    "LastName",
    "Password",
)
