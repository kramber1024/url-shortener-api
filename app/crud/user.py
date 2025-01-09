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
    """Create a new ` User ` and commit it to the database.

    Args:
        async_session: The async database session.
        first_name: The first name of the user.
        last_name: The last name of the user.
        email: The email address of the user.
        password: The raw password of the user.

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
    """Retrieve a ` User ` from the database by their id.

    Args:
        async_session: The async database session.
        user_id: The unique identifier of the ` User ` to retrieve.

    Returns:
        The ` User ` instance if found, otherwise ` None `.
    """
    result: Result[tuple[User]] = await async_session.execute(
        select(User).where(User.id == user_id),
    )
    user: User | None = result.scalars().first()

    return user


async def get_user_by_email(
    *,
    async_session: AsyncSession,
    email: str,
) -> User | None:
    """Retrieve a ` User ` from the database by their email address.

    Args:
        async_session: The async database session.
        email: The email address of the ` User ` to retrieve.

    Returns:
        The ` User ` instance if found, otherwise ` None `.
    """
    result: Result[tuple[User]] = await async_session.execute(
        select(User).where(User.email == email),
    )
    user: User | None = result.scalars().first()

    return user
