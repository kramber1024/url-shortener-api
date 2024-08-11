from typing import Annotated, Literal

from pydantic import BaseModel, Field

from app.api.schemes.fields import Email, FirstName, HTTPStatus, Id, LastName, Password
from app.core.database import models


class Error(BaseModel):
    message: Annotated[
        str,
        Field(
            description="Error message. Should not be used as feedback for a user.",
            examples=["Password length is incorrect"],
        ),
    ]
    type: Annotated[
        str,
        Field(
            description=(
                "Error type. Should be used for frontend logic e.g. form validation."
            ),
            examples=["password"],
        ),
    ]


class ErrorResponse(BaseModel):
    errors: Annotated[
        list[Error],
        Field(
            description="List of errors.",
        ),
    ]
    message: Annotated[
        str,
        Field(
            description="Generic error message.",
            examples=["Validation error"],
        ),
    ]
    status: HTTPStatus


class SuccessResponse(BaseModel):
    message: Annotated[
        str,
        Field(
            description="Success message.",
            examples=["Operation completed successfully"],
        ),
    ]
    status: HTTPStatus


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


__all__ = (
    "Error",
    "ErrorResponse",
    "SuccessResponse",
    "User",
    "UserLogin",
    "UserRegistration",
)
