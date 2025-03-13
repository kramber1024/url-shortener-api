import pytest

from app.core.database.models import Click
from app.core.settings.data import IP, Country


@pytest.fixture(scope="module")
def url_id() -> int:
    return 1


@pytest.fixture(scope="module")
def ip() -> str:
    return "127.0.0.1"


@pytest.fixture(scope="module")
def country() -> str:
    return "se"


def test_click_init(url_id: int, ip: str, country: str) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    assert click.url_id == url_id
    assert click.ip == ip
    assert click.country == country


@pytest.mark.parametrize("url_id", [123321, 77850370187, 14991194284, -1, 0])
def test_click_property_url_id(url_id: int, ip: str, country: str) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    assert click.url_id == url_id


@pytest.mark.parametrize(
    "ip",
    [
        "192.168.0.1",
        "10.0.0.1",
        "172.16.0.1",
        "199.2.6.8",
        None,
    ],
)
def test_click_property_ip(url_id: int, ip: str | None, country: str) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    assert click.ip == ip


@pytest.mark.parametrize(
    "ip",
    [
        "a" * (IP.MIN_LENGTH - 1),
        "a" * (IP.MAX_LENGTH + 1),
        "a" * (IP.MAX_LENGTH + 100),
        "0000.0000.0000.0000",
        "",
    ],
)
def test_click_property_ip_invalid_length(
    url_id: int,
    ip: str,
    country: str,
) -> None:
    click: Click = Click(url_id=url_id, ip="127.0.0.1", country=country)

    with pytest.raises(ValueError, match="^$"):
        click.ip = ip


@pytest.mark.parametrize(
    "ip",
    [
        "a" * (IP.MIN_LENGTH + 1),
        "a" * (IP.MAX_LENGTH - 1),
        "a" * IP.MIN_LENGTH,
        "a" * IP.MAX_LENGTH,
        "127.127.127.127",
    ],
)
def test_click_property_ip_valid_length(
    url_id: int,
    ip: str,
    country: str,
) -> None:
    click: Click = Click(url_id=url_id, ip="127.0.0.1", country=country)

    click.ip = ip

    assert click.ip == ip


@pytest.mark.parametrize(
    "country",
    [
        "us",
        "ca",
        "ru",
        "se",
        None,
    ],
)
def test_click_property_country(
    url_id: int,
    ip: str,
    country: str | None,
) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    assert click.country == country


@pytest.mark.parametrize(
    "country",
    [
        "kra",
        "mbe",
        "reb",
        "a" * (Country.MAX_LENGTH + 1),
        "a" * (Country.MIN_LENGTH - 1),
    ],
)
def test_click_property_country_invalid_length(
    url_id: int,
    ip: str,
    country: str,
) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country="US")

    with pytest.raises(ValueError, match="^$"):
        click.country = country


@pytest.mark.parametrize(
    "country",
    [
        "us",
        "ca",
        "ru",
        "se",
        "ar",
    ],
)
def test_click_property_country_valid_length(
    url_id: int,
    ip: str,
    country: str,
) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country="ru")

    click.country = country

    assert click.country == country


def test_click_repr(url_id: int, ip: str, country: str) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    assert repr(click) == f"<Click {click.id} from {country}>"
