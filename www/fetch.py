"""This module contains functions for fetching data from the repository."""

from typing import Any, Literal

from httpx import AsyncClient, Response

from app.core.database.models import Network

from .parse import parse_country, parse_download_url, parse_network


async def fetch_download_urls(
    *,
    directory: Literal["ipv4", "ipv6"],
    async_client: AsyncClient,
) -> list[str]:
    """Fetch the download URLs for IP block lists from a given directory.

    See [**api response**
    ](https://api.github.com/repos/herrbischoff/country-ip-blocks/contents/ipv4
    ) for ` ipv4 ` directory.

    Args:
        directory: The directory to fetch download URLs from.
        async_client: The async HTTP client to use.

    Returns:
        A list of download URLs for IP block lists.
    """
    response: Response = await async_client.get(
        "https://api.github.com/repos/"
        f"herrbischoff/country-ip-blocks/contents/{directory}",
    )
    json: Any = response.json()

    if not isinstance(json, list):
        return []

    return list(filter(None, map(parse_download_url, json)))


async def fetch_networks(
    *,
    download_url: str,
    async_client: AsyncClient,
) -> list[Network]:
    """Fetch list of networks from a download URL.

    Args:
        download_url: The download URL to fetch networks from.
        async_client: The async HTTP client to use.

    Returns:
        A list of networks.
    """
    response: Response = await async_client.get(download_url)

    return list(
        filter(
            None,
            [
                parse_network(line, country=parse_country(download_url))
                for line in response.text.splitlines()
            ],
        ),
    )


__all__ = ["fetch_download_urls", "fetch_networks"]
