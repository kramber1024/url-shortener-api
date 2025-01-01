"""Networks fetch module."""

from typing import Any

from httpx import AsyncClient, Response

from app.core.database.models import Network


def _parse_download_url(content: object, /) -> str | None:
    if (
        not isinstance(content, dict)
        or "download_url" not in content
        or not isinstance(content["download_url"], str)
    ):
        return None

    return content["download_url"]


async def fetch_download_urls(
    *,
    directory: str,
    async_client: AsyncClient,
) -> list[str]:
    """Fetch download URL's from GitHub API.

    Args:
        directory: The directory to fetch download URL's from.
        async_client: The async HTTP client to use.

    Returns:
        A list of download URL's.
    """
    response: Response = await async_client.get(
        "https://api.github.com/repos/"
        f"herrbischoff/country-ip-blocks/contents/{directory}",
    )
    json: Any = response.json()

    if not isinstance(json, list):
        return []

    return list(filter(None, map(_parse_download_url, json)))


async def fetch_networks(
    *,
    download_url: str,
    async_client: AsyncClient,
) -> list[Network]:
    """Fetch networks from a download URL.

    Args:
        download_url: The download URL to fetch networks from.
        async_client: The async HTTP client to use.

    Returns:
        A list of networks.
    """
    response: Response = await async_client.get(download_url)

    networks: list[Network] = []
    for line in response.text.splitlines():
        try:
            networks.append(
                Network(
                    address=line.split("/")[0],
                    mask=int(line.split("/")[1]),
                    country=download_url.split("/")[-1].split(".")[0],
                ),
            )
        except (IndexError, ValueError):
            continue

    return networks


__all__ = ["fetch_download_urls", "fetch_networks"]
