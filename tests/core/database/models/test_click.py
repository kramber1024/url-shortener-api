import pytest

from app.core.database.models import Click
from app.core.settings.data import Country


@pytest.fixture(scope="module")
def url_id() -> int:
    return 1


@pytest.fixture(scope="module")
def ip() -> str:
    return "192.168.0.1"


@pytest.fixture(scope="module")
def country() -> str:
    return "ru"


@pytest.fixture()
def click() -> Click:
    return Click(url_id=1, ip="127.0.0.1", country="es")


@pytest.mark.parametrize("url_id", [0, 1, 2])
@pytest.mark.parametrize("ip", ["192.168.0.1", "127.0.0.1", None])
@pytest.mark.parametrize(
    "country",
    ["r" * Country.MAX_LENGTH, "e" * Country.MIN_LENGTH, None],
)
def test_click_init(url_id: int, ip: str | None, country: str | None) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    assert click._url_id == url_id
    assert click.ip == ip
    assert click.country == country


@pytest.mark.parametrize("url_id", [0, 1, 2])
def test_click_property_url_id(url_id: int, ip: str, country: str) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    assert click.url_id == url_id


@pytest.mark.parametrize("ip", ["192.168.0.1", "127.0.0.1", None])
def test_click_property_ip(url_id: int, ip: str | None, country: str) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    assert click.ip == ip


@pytest.mark.parametrize("ip", ["192.168.0.1", "10.0.0.1", None])
def test_click_property_ip_setter(ip: str, click: Click) -> None:
    click.ip = ip

    assert click.ip == ip


@pytest.mark.parametrize("ip", ["", "2560.256.256.256", "1.1.1."])
def test_click_property_ip_setter_invalid_length(ip: str, click: Click) -> None:
    with pytest.raises(ValueError, match="^$"):
        click.ip = ip


@pytest.mark.parametrize(
    "country",
    ["U" * Country.MAX_LENGTH, "A" * Country.MIN_LENGTH, None],
)
def test_click_property_country(
    url_id: int,
    ip: str,
    country: str | None,
) -> None:
    click: Click = Click(url_id=url_id, ip=ip, country=country)

    assert click.country == country


@pytest.mark.parametrize("country", ["us", "ru", None])
def test_click_property_country_setter(country: str, click: Click) -> None:
    click.country = country

    assert click.country == country


@pytest.mark.parametrize(
    "country",
    ["", "USA", "r" * (Country.MAX_LENGTH + 1), "e" * (Country.MIN_LENGTH - 1)],
)
def test_click_property_country_setter_invalid_length(
    country: str,
    click: Click,
) -> None:
    with pytest.raises(ValueError, match="^$"):
        click.country = country


def test_click_repr(click: Click) -> None:
    assert repr(click) == f"<Click {click.ip} from {click.country}>"
