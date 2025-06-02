from typing import Annotated, Literal

from pydantic import BaseModel, EmailStr, Field, StringConstraints

from app.core.database import models
from app.core.settings.data import Email, FirstName, LastName, Password

from .fields import Id


class _BaseUser(BaseModel):
    email: Annotated[
        EmailStr,
        StringConstraints(
            strip_whitespace=True,
            min_length=Email.MIN_LENGTH,
            max_length=Email.MAX_LENGTH,
        ),
        Field(
            description="User's email address for login and notifications.",
            examples=["john.doe@example.com"],
        ),
    ]


class _BaseUserWithName(_BaseUser):
    first_name: Annotated[
        str,
        StringConstraints(
            strip_whitespace=True,
            min_length=FirstName.MIN_LENGTH,
            max_length=FirstName.MAX_LENGTH,
        ),
        Field(
            description="User's first name.",
            examples=["John"],
        ),
    ]
    last_name: Annotated[
        str | None,
        StringConstraints(
            strip_whitespace=True,
            min_length=LastName.MIN_LENGTH,
            max_length=LastName.MAX_LENGTH,
        ),
        Field(
            description="User's last name.",
            examples=["Doe"],
        ),
    ] = None


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
    password: Annotated[
        str,
        StringConstraints(
            min_length=Password.MIN_LENGTH,
            max_length=Password.MAX_LENGTH,
        ),
        Field(
            description="User's password for authentication.",
            examples=["password"],
        ),
    ]


class CreateUser(LoginUser, _BaseUserWithName):
    terms: Annotated[
        Literal["on"],
        Field(
            description=(
                "Confirmation of terms of service acceptance."
                "Only accepted value is **on**."
            ),
            examples=["on"],
        ),
    ]
