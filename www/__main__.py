import asyncio
from typing import TYPE_CHECKING

from httpx import AsyncClient, Timeout

from app.core.database import database
from app.core.logger import logger

from .fetch import fetch_download_urls, fetch_networks

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

    from app.core.database.models import Network


async def main() -> None:
    await database.create_tables(hard_reset=False)
    async_session: AsyncSession = await anext(database.get_async_session())

    logger.info("Parsing network data from GitHub API.")
    async with AsyncClient(timeout=Timeout(timeout=9, pool=60)) as async_client:
        download_urls: list[str] = await fetch_download_urls(
            directory="ipv4",
            async_client=async_client,
        )
        logger.info(f"Found {len(download_urls)}/241 download URL's.")

        results: list[list[Network]] = await asyncio.gather(
            *[
                fetch_networks(
                    download_url=download_url,
                    async_client=async_client,
                )
                for download_url in download_urls
            ],
        )
        for networks in results:
            async_session.add_all(networks)
            await async_session.commit()

            logger.info(
                f"Successfully processed {len(networks)} networks from "
                f"{networks[0].country}.",
            )


if __name__ == "__main__":
    asyncio.run(main())
