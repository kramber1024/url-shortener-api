"""Module for parsing data from the Github API responses."""

from app.core.database.models import Network


def parse_country(download_url: str, /) -> str:
    """Parse the country from the download URL.

    Args:
        download_url: The download URL to parse the country from.

    Returns:
        The ISO 3166-1 country code.
    """
    return download_url.split("/")[-1].split(".")[0]


def parse_download_url(content: object, /) -> str | None:
    """Try to parse the download URL from the API response.

    Args:
        content: The API response.

    Returns:
        The download URL if found, otherwise ` None `.
    """
    if (
        not isinstance(content, dict)
        or "download_url" not in content
        or not isinstance(content["download_url"], str)
    ):
        return None

    return content["download_url"]


def parse_network(line: str, /, *, country: str) -> Network | None:
    """Parse a ` Network ` from a string.

    Args:
        line: The string to parse the ` Network ` from.
        country: The country code of the ` Network `.

    Returns:
        The ` Network ` if parsed successfully, otherwise ` None `.
    """
    try:
        address, mask = line.split("/")
        return Network(
            address=address,
            mask=int(mask),
            country=country,
        )

    except ValueError:
        return None


__all__ = ["parse_country", "parse_download_url", "parse_network"]
