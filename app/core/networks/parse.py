"""View the README.md file from the current directory."""

import asyncio
from typing import TYPE_CHECKING

from httpx import AsyncClient, HTTPError, Response
from sqlalchemy.exc import IntegrityError

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


def _get_countries(response: Response) -> list[str]:
    return [country["name"].split(".")[0] for country in response.json()]


def _get_cidrs(response: Response) -> list[str]:
    return response.text.splitlines()


async def parse(*, cooldown: int = 5) -> None:
    logger.info("Parsing network data from GitHub API.")

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

                for j, cidr in enumerate(cidrs):
                    logger.info(
                        f"Processing {cidr}. ({j + 1}/{len(cidrs)})",
                    )
                    session: AsyncSession = db.session_factory()

                    try:
                        await crud.create_network(
                            session=session,
                            address=cidr.split("/")[0],
                            mask=int(cidr.split("/")[1]),
                            country=country,
                        )
                        await session.commit()

                    except IntegrityError:
                        logger.warning(
                            f"Network {cidr.split("/")[0]} already exists in the "
                            "database.",
                        )
                        await session.rollback()

                    finally:
                        await session.close()

                await asyncio.sleep(cooldown)

        except HTTPError as http_error:
            logger.error(f"HTTP error occurred: {http_error}")


if __name__ == "__main__":
    asyncio.run(parse(cooldown=5))
