from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, EmailStr, Field

from app.api.schemes.fields import Id
from app.core.database import models

_FirstName: TypeAlias = Annotated[
    str,
    Field(
        min_length=3,
        max_length=16,
        description="Used in full name and official emails",
        examples=["John"],
    ),
]

_LastName: TypeAlias = Annotated[
    str,
    Field(
        min_length=3,
        max_length=16,
        description="Used in full name.",
        examples=["Doe"],
    ),
]

_Email: TypeAlias = Annotated[
    EmailStr,
    Field(
        min_length=len("*@*.*"),
        max_length=64,
        description="Email used for authentication and notifications.",
        examples=["email@domain.tld"],
    ),
]

_Password: TypeAlias = Annotated[
    str,
    Field(
        min_length=8,
        max_length=256,
        description="Used for authentication.",
        examples=["My$uper$ecretPa$$word"],
    ),
]


class User(BaseModel):
    id: Id
    first_name: _FirstName
    last_name: _LastName | None = None
    email: _Email

    @classmethod
    def from_model(cls: type["User"], user: models.User) -> "User":
        return cls(
            id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )


class UserLogin(BaseModel):
    email: _Email
    password: _Password


class UserRegistration(BaseModel):
    first_name: _FirstName
    last_name: _LastName | None = None
    email: _Email
    password: _Password
    terms: Annotated[
        Literal["on"],
        Field(
            description="User agreement to terms of use.",
            examples=["on"],
        ),
    ]
