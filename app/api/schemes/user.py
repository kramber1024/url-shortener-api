from typing import Annotated, Literal

from pydantic import BaseModel, Field

from app.api.schemes.fields import Email, FirstName, Id, LastName, Password
from app.core.database import models


class User(BaseModel):
    id: Id
    first_name: FirstName
    last_name: LastName | None = None
    email: Email

    @classmethod
    def from_model(cls: type["User"], user: models.User) -> "User":
        return cls(
            id=str(user.id),
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
        )


class UserLogin(BaseModel):
    email: Email
    password: Password


class UserRegistration(BaseModel):
    first_name: FirstName
    last_name: LastName | None = None
    email: Email
    password: Password
    terms: Annotated[
        Literal["on"],
        Field(
            description="User agreement to terms of use.",
            examples=["on"],
        ),
    ]
