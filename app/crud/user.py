from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import User

if TYPE_CHECKING:
    from sqlalchemy import Result


async def create_user(
    *,
    async_session: AsyncSession,
    first_name: str,
    last_name: str | None,
    email: str,
    password: str,
) -> User:
    """Create a new user and commit it to the database.

    Args:
        async_session (AsyncSession): The database session.
        first_name (str): The first name of the user.
        last_name (str | None): The last name of the user. Can be None.
        email (str): The email address of the user.
        password (str): Plain text password of the user. \
            Password will be hashed before commiting it to the database.

    Returns:
        The newly created ` User ` instance.
    """
    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)
    return user


async def get_user_by_id(
    *,
    async_session: AsyncSession,
    user_id: int,
) -> User | None:
    """Retrieve a user from the database by their ` id `.

    Args:
        async_session (AsyncSession): The database session.
        user_id (int): The ` id ` of the user to retrieve.

    Returns:
        The ` User ` instance if found, otherwise ` None `.
    """
    result: Result[tuple[User]] = await async_session.execute(
        select(User).filter(User.id == user_id),
    )
    user: User | None = result.scalars().first()

    return user


async def get_user_by_email(
    *,
    async_session: AsyncSession,
    email: str,
) -> User | None:
    """Retrieve a user from the database by their ` email ` address.

    Args:
        async_session (AsyncSession): The database session.
        email (str): The ` email ` address of the user to retrieve.

    Returns:
        The ` User ` instance if found, otherwise ` None `.
    """
    result: Result[tuple[User]] = await async_session.execute(
        select(User).where(User.email == email),
    )
    user: User | None = result.scalars().first()

    return user
