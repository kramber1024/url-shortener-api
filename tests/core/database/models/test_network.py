import pytest

from app.core.database.models import Network


@pytest.fixture(scope="module")
def address() -> str:
    return "168.217.152.0"


@pytest.fixture(scope="module")
def mask() -> int:
    return 24


@pytest.fixture(scope="module")
def country() -> str:
    return "xx"


@pytest.mark.parametrize(
    "address",
    [
        "255.255.255.255",
        "333.333.333.333",
        "1.1..1.1",
        "65e3:f9e8:6ed5:3c74:77ea:0824:f8b5:1b07",
        "fbae7e6b3da4edc4e45a59e04e4e08731983efd3",
    ],
)
def test_network_init_invalid_address(
    address: str,
    mask: int,
    country: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=rf"'{address}/{mask}' does not appear to be an IPv4 network",
    ):
        Network(address=address, mask=mask, country=country)


@pytest.mark.parametrize(
    "address",
    [
        "167.246.10.0",
        "80.144.15.0",
        "1.211.136.0",
        "11.82.247.0",
        "150.85.8.0",
    ],
)
def test_network_init_valid_address(
    address: str,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network._address == address


@pytest.mark.parametrize(
    "mask",
    [
        0,
        33,
        128,
        255,
        256,
    ],
)
def test_network_init_invalid_mask(
    address: str,
    mask: int,
    country: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=rf"'{address}/{mask}' does not appear to be an IPv4 network",
    ):
        Network(address=address, mask=mask, country=country)


@pytest.mark.parametrize(
    "mask",
    [
        8,
        16,
        24,
        32,
    ],
)
def test_network_init_valid_mask(
    mask: int,
    country: str,
) -> None:
    address: str = "192.0.0.0"

    network: Network = Network(address=address, mask=mask, country=country)

    assert network._mask == mask


@pytest.mark.parametrize(
    "country",
    [
        "11",
        "xxx",
        "abcd",
        "e",
        "",
    ],
)
def test_network_init_invalid_country(
    address: str,
    mask: int,
    country: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=rf"Invalid country code '{country}'",
    ):
        Network(address=address, mask=mask, country=country)


@pytest.mark.parametrize(
    "country",
    [
        "ru",
        "us",
        "mx",
        "br",
        "ar",
    ],
)
def test_network_init_valid_country(
    address: str,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network._country == country


def test_network_init(
    address: str,
    mask: int,
    country: str,
) -> None:
    start_address: int = 2832832512
    end_address: int = 2832832767

    network: Network = Network(address=address, mask=mask, country=country)

    assert network._start_address == start_address
    assert network._end_address == end_address
    assert network._address == address
    assert network._mask == mask
    assert network._country == country


def test_network_property_id(
    address: str,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert hasattr(network, "_id")
    assert hasattr(network, "id")


@pytest.mark.parametrize(
    ("address", "start_address"),
    [
        ("82.107.183.0", 1382790912),
        ("231.243.199.0", 3891513088),
        ("246.78.52.0", 4132320256),
        ("224.84.0.0", 3763601408),
        ("16.0.221.0", 268492032),
    ],
)
def test_network_property_start_address(
    address: str,
    start_address: int,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network._start_address == start_address
    assert network.start_address == start_address


@pytest.mark.parametrize(
    ("address", "end_address"),
    [
        ("137.133.163.0", 2307236863),
        ("91.65.118.0", 1531016959),
        ("109.153.0.0", 1838743807),
        ("1.0.1.0", 16777727),
        ("253.87.207.0", 4250390527),
    ],
)
def test_network_property_end_address(
    address: str,
    end_address: int,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network._end_address == end_address
    assert network.end_address == end_address


def test_network_property_country(
    address: str,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network._country == country
    assert network.country == country


def test_network_property_address(
    address: str,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network._address == address
    assert network.address == address


def test_network_property_mask(
    address: str,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network._mask == mask
    assert network.mask == mask


def test_network_property_cidr(
    address: str,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network.cidr == f"{address}/{mask}"


def test_network_repr(
    address: str,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert repr(network) == f"<Network {address}/{mask} {country}>"
