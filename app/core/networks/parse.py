"""View the README.md file from the current directory."""

import asyncio
from typing import TYPE_CHECKING

from httpx import AsyncClient

from app.core.database import database
from app.core.logger import logger
from app.core.networks.fetch import fetch_download_urls, fetch_networks

if TYPE_CHECKING:
    from app.core.database.models import Network


async def parse() -> None:
    logger.info("Parsing network data from GitHub API.")

    async with AsyncClient(timeout=5) as async_client:
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
        for i, networks in enumerate(results, start=1):
            async with database.get_async_session() as async_session:
                async_session.add_all(networks)
                await async_session.commit()

            logger.info(
                f"Successfully processed {len(networks)} networks from "
                f"{download_urls[i - 1].split('/')[-1].split('.')[0]}. "
                f"({i}/{len(download_urls)})",
            )


if __name__ == "__main__":
    asyncio.run(parse())
