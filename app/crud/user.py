from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import User


async def create_user(
    *,
    session: AsyncSession,
    first_name: str,
    last_name: str | None,
    email: str,
    password: str,
) -> User:
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


async def get_user_by_email(
    *,
    session: AsyncSession,
    email: str,
) -> User | None:
    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.email == email),
    )
    user: User | None = result.scalars().first()

    return user


async def get_user_by_id(
    *,
    session: AsyncSession,
    id_: int,
) -> User | None:
    result: Result[tuple[User]] = await session.execute(
        select(User).filter(User.id == id_),
    )
    user: User | None = result.scalars().first()

    return user
