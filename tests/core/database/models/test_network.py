from ipaddress import IPv4Network

import pytest

from app.core.database.models import Network


@pytest.fixture(scope="module")
def address() -> str:
    return "192.168.0.0"


@pytest.fixture(scope="module")
def mask() -> int:
    return 24


@pytest.fixture(scope="module")
def country() -> str:
    return "es"


@pytest.fixture()
def network(address: str, mask: int, country: str) -> Network:
    return Network(address=address, mask=mask, country=country)


@pytest.mark.parametrize("address", ["192.168.0.0", "127.0.0.0", "172.0.0.0"])
@pytest.mark.parametrize("mask", [16, 24, 32])
@pytest.mark.parametrize("country", ["ru", "en", "ca"])
def test_network_init(address: str, mask: int, country: str) -> None:
    ipv4_network: IPv4Network = IPv4Network(f"{address}/{mask}")

    network: Network = Network(address=address, mask=mask, country=country)

    assert network._start_address == int(ipv4_network.network_address)
    assert network._end_address == int(ipv4_network.broadcast_address)
    assert network._country == country
    assert network._address == address
    assert network._mask == mask


@pytest.mark.parametrize("address", ["1227.9.9.9", "256.256.256.256", "1.1.1."])
def test_network_init_invalid_address(
    address: str,
    mask: int,
    country: str,
) -> None:
    with pytest.raises(ValueError, match=".*"):
        Network(address=address, mask=mask, country=country)


@pytest.mark.parametrize("mask", [-1, 0, 33])
def test_network_init_invalid_mask(
    address: str,
    mask: int,
    country: str,
) -> None:
    with pytest.raises(ValueError, match=".*"):
        Network(address=address, mask=mask, country=country)


@pytest.mark.parametrize("country", ["1", "12", "ENN", "r"])
def test_network_init_invalid_country(
    address: str,
    mask: int,
    country: str,
) -> None:
    with pytest.raises(ValueError, match=".*"):
        Network(address=address, mask=mask, country=country)


def test_network_property_id(network: Network) -> None:
    assert network.id is None


@pytest.mark.parametrize("address", ["192.168.1.0", "10.20.30.0", "172.16.1.0"])
def test_network_property_start_address(
    address: str,
    mask: int,
    country: str,
) -> None:
    ipv4_network: IPv4Network = IPv4Network(f"{address}/{mask}")

    network: Network = Network(address=address, mask=mask, country=country)

    assert network.start_address == int(ipv4_network.network_address)


@pytest.mark.parametrize("address", ["192.168.1.0", "10.20.30.0", "172.16.1.0"])
def test_network_property_end_address(
    address: str,
    mask: int,
    country: str,
) -> None:
    ipv4_network: IPv4Network = IPv4Network(f"{address}/{mask}")

    network: Network = Network(address=address, mask=mask, country=country)

    assert network.end_address == int(ipv4_network.broadcast_address)


@pytest.mark.parametrize("country", ["US", "ru", "Xx"])
def test_network_property_country(
    address: str,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network.country == country


@pytest.mark.parametrize("address", ["192.168.1.0", "10.20.30.0", "172.16.1.0"])
def test_network_property_address(
    address: str,
    mask: int,
    country: str,
) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network.address == address


@pytest.mark.parametrize("mask", [16, 24, 32])
def test_network_property_mask(address: str, mask: int, country: str) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network.mask == mask


@pytest.mark.parametrize("address", ["192.168.1.0", "10.20.30.0", "172.16.1.0"])
@pytest.mark.parametrize("mask", [24, 32])
def test_network_property_cidr(address: str, mask: int, country: str) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert network.cidr == f"{address}/{mask}"


@pytest.mark.parametrize("address", ["192.168.0.0", "127.0.0.0", "172.0.0.0"])
@pytest.mark.parametrize("mask", [16, 24, 32])
@pytest.mark.parametrize("country", ["ru", "en", "ca"])
def test_network_repr(address: str, mask: int, country: str) -> None:
    network: Network = Network(address=address, mask=mask, country=country)

    assert repr(network) == f"<Network {address}/{mask} {country}>"
