from typing import Annotated, Literal, TypeAlias

from pydantic import BaseModel, EmailStr, Field, StringConstraints

from app.api.schemes.fields import Id
from app.core.config import settings
from app.core.database import models

_FirstName: TypeAlias = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=settings.data.FIRST_NAME_MIN_LENGTH,
        max_length=settings.data.FIRST_NAME_MAX_LENGTH,
    ),
    Field(
        description="Used in full name and official emails",
        examples=["John"],
    ),
]

_LastName: TypeAlias = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=settings.data.LAST_NAME_MIN_LENGTH,
        max_length=settings.data.LAST_NAME_MAX_LENGTH,
    ),
    Field(
        description="Used in full name.",
        examples=["Doe"],
    ),
]

_Email: TypeAlias = Annotated[
    EmailStr,
    StringConstraints(
        min_length=settings.data.EMAIL_MIN_LENGTH,
        max_length=settings.data.EMAIL_MAX_LENGTH,
    ),
    Field(
        description="Email used for authentication and notifications.",
        examples=["email@domain.tld"],
    ),
]

_Password: TypeAlias = Annotated[
    str,
    StringConstraints(
        min_length=settings.data.PASSWORD_MIN_LENGTH,
        max_length=settings.data.PASSWORD_MAX_LENGTH,
    ),
    Field(
        description="Used for authentication.",
        examples=["My$uper$ecretPa$$word"],
    ),
]

_Terms: TypeAlias = Annotated[
    Literal["on"],
    Field(
        description="User agreement to terms of use.",
        examples=["on"],
    ),
]


class _BaseUser(BaseModel):
    email: _Email


class _BaseUserWithName(_BaseUser):
    first_name: _FirstName
    last_name: _LastName | None = None


class User(_BaseUserWithName):
    id: Id

    @classmethod
    def from_model(cls: type["User"], user: models.User) -> "User":
        return cls(
            id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )


class LoginUser(_BaseUser):
    password: _Password


class CreateUser(LoginUser, _BaseUserWithName):
    terms: _Terms
