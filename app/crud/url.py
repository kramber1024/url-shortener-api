from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.models import Url


async def create_url(
    *,
    session: AsyncSession,
    user_id: int,
    address: str,
    location: str,
) -> Url:
    url: Url = Url(
        user_id=user_id,
        address=address,
        location=location,
    )

    session.add(url)
    await session.commit()
    await session.refresh(url)
    return url
