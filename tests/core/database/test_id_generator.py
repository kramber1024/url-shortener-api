import pytest
from snowflake import SnowflakeGenerator

from app.core.database.id_generator import IdGenerator


@pytest.fixture(scope="module")
def machine_id() -> int:
    return 1


@pytest.fixture()
def id_generator(machine_id: int) -> IdGenerator:
    return IdGenerator(machine_id=machine_id)


def test_id_generator_init(machine_id: int) -> None:
    id_generator: IdGenerator = IdGenerator(machine_id=machine_id)

    assert isinstance(id_generator._snowflake_generator, SnowflakeGenerator)
    assert id_generator._snowflake_generator._inf == machine_id << 12


def test_id_generator_call(id_generator: IdGenerator) -> None:
    snowflake_id: int = id_generator()

    assert isinstance(snowflake_id, int)


def test_id_generator_call_unique(id_generator: IdGenerator) -> None:
    snowflake_id_1: int = id_generator()
    snowflake_id_2: int = id_generator()

    assert snowflake_id_1 != snowflake_id_2
