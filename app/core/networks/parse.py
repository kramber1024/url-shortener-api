"""View the README.md file from the current directory."""

import asyncio
from typing import TYPE_CHECKING

from httpx import AsyncClient, HTTPError, Response

from app import crud
from app.core.database import db
from app.core.logger import logger

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

_API_BASE: str = "https://api.github.com/repositories/114153288/contents"
_COUNTRIES_DIRECTORY: str = "ipv4"
_RAW_BASE: str = (
    "https://raw.githubusercontent.com/herrbischoff/country-ip-blocks/refs/heads/master"
)
_BIG_BLOCK: int = 500


def _get_countries(response: Response) -> list[str]:
    return [country["name"].split(".")[0] for country in response.json()]


def _get_cidrs(response: Response) -> list[str]:
    return response.text.splitlines()


async def parse(*, cooldown: int = 5) -> None:
    logger.info("Parsing network data from GitHub API.")
    session: AsyncSession = db.session_factory()

    async with AsyncClient(timeout=5) as client:
        try:
            countries_response: Response = await client.get(
                f"{_API_BASE}/{_COUNTRIES_DIRECTORY}",
            )
            countries: list[str] = _get_countries(countries_response)
            logger.info(f"Successfully fetched {len(countries)} countries.")

            for i, country in enumerate(countries):
                logger.info(
                    f"Fetching CIDR's for {country.upper()}. "
                    f"({i + 1}/{len(countries)})",
                )
                cidr_response: Response = await client.get(
                    f"{_RAW_BASE}/{_COUNTRIES_DIRECTORY}/{country}.cidr",
                )
                cidrs: list[str] = _get_cidrs(cidr_response)
                logger.info(
                    f"Successfully fetched networks for {country.upper()}. "
                    f"Found {len(cidrs)} CIDR's.",
                )

                log_step: int = 10 if len(cidrs) < _BIG_BLOCK else 100
                for j, cidr in enumerate(cidrs):
                    if j % log_step == 0 or j == len(cidrs) - 1:
                        logger.info(
                            f"Processing {cidr}. ({j + 1}/{len(cidrs)})",
                        )

                    await crud.create_network(
                        session=session,
                        network=cidr.split("/")[0],
                        mask=int(cidr.split("/")[1]),
                        country=country,
                    )
                await session.commit()
                logger.info(
                    f"Successfully processed all {len(cidrs)} CIDR's "
                    f"from {country.upper()}.",
                )

                await asyncio.sleep(cooldown)

        except HTTPError as http_error:
            logger.error(f"HTTP error occurred: {http_error}")


if __name__ == "__main__":
    asyncio.run(parse(cooldown=5))
