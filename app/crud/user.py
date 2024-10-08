from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import User

if TYPE_CHECKING:
    from sqlalchemy import Result


async def create_user(
    *,
    session: AsyncSession,
    first_name: str,
    last_name: str | None,
    email: str,
    password: str,
) -> User:
    """Create a new user and commit it to the database.

    Args:
        session (AsyncSession): The database session.
        first_name (str): The first name of the user.
        last_name (str | None): The last name of the user. Can be None.
        email (str): The email address of the user.
        password (str): Plain text password of the user. \
            Password will be hashed before commiting it to the database.

    Returns:
        The newly created ` User ` instance.

    Example:
        >>> user = await create_user(
        ...    session=session,
        ...     first_name="John",
        ...     last_name=None,
        ...     email="john.doe@example.com",
        ...     password="securepassword"
        ... )
    """
    user: User = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def get_user_by_id(
    *,
    session: AsyncSession,
    id_: int,
) -> User | None:
    """Retrieve a user from the database by their ` id `.

    Args:
        session (AsyncSession): The database session.
        id_ (int): The ` id ` of the user to retrieve.

    Returns:
        The ` User ` instance if found, otherwise ` None `.

    Example:
        >>> user = await get_user_by_id(
        ...     session=session,
        ...     id_=1,
        ... )
        >>> if user:
        >>>     print(f"User found: {user.display_name}")
        >>> else:
        >>>     print("User not found.")
    """
    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.id == id_),
    )
    user: User | None = result.scalars().first()

    return user


async def get_user_by_email(
    *,
    session: AsyncSession,
    email: str,
) -> User | None:
    """Retrieve a user from the database by their ` email ` address.

    Args:
        session (AsyncSession): The database session.
        email (str): The ` email ` address of the user to retrieve.

    Returns:
        The ` User ` instance if found, otherwise ` None `.

    Example:
        >>> user = await get_user_by_email(
        ...     session=session,
        ...     email="john.doe@example.com",
        ... )
        >>> if user:
        >>>     print(f"User found: {user.display_name}")
        >>> else:
        >>>     print("User not found.")
    """
    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == email),
    )
    user: User | None = result.scalars().first()

    return user
