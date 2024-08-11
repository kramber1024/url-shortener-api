from typing import Annotated, TypeAlias

from pydantic import EmailStr, Field

__all__ = (
    "Email",
    "FirstName",
    "HTTPStatus",
    "Id",
    "LastName",
    "Password",
)

Email: TypeAlias = Annotated[
    EmailStr,
    Field(
        min_length=len("*@*.*"),
        max_length=64,
        description="Email used for authentication and notifications.",
        examples=["email@domain.tld"],
    ),
]

FirstName: TypeAlias = Annotated[
    str,
    Field(
        min_length=3,
        max_length=16,
        description="Used in full name and official emails",
        examples=["John"],
    ),
]

HTTPStatus: TypeAlias = Annotated[
    int,
    Field(
        description="HTTP status code.",
        examples=[422],
        ge=100,
        le=599,
    ),
]

Id: TypeAlias = Annotated[
    str,
    Field(
        description="Unique identifier.",
        examples=["7205626878688008192"],
        max_length=len("7205626878688008192"),
        min_length=len("7205626878688008192"),
    ),
]


LastName: TypeAlias = Annotated[
    str,
    Field(
        min_length=3,
        max_length=16,
        description="Used in full name.",
        examples=["Doe"],
    ),
]

Password: TypeAlias = Annotated[
    str,
    Field(
        min_length=8,
        max_length=256,
        description="Used for authentication.",
        examples=["My$uper$ecretPa$$word"],
    ),
]
