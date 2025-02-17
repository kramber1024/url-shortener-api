import pytest

from app.core.settings.data import Data


def test_data_without_attributes() -> None:
    with pytest.raises(AttributeError):

        class InvalidData(Data): ...


def test_data_with_extra_attributes() -> None:
    with pytest.raises(AttributeError):

        class InvalidData(Data):
            EXTRA_ATTRIBUTE: str = "EXTRA_ATTRIBUTE"


def test_data_without_min_length_attribute() -> None:
    with pytest.raises(AttributeError):

        class InvalidData(Data):
            MAX_LENGTH: int = 0


def test_data_without_max_length_attribute() -> None:
    with pytest.raises(AttributeError):

        class InvalidData(Data):
            MIN_LENGTH: int = 0


def test_data_with_min_length_and_max_length_attributes() -> None:
    class ValidData(Data):
        MIN_LENGTH: int = 0
        MAX_LENGTH: int = 1

    assert ValidData.MIN_LENGTH == 0
    assert ValidData.MAX_LENGTH == 1


def test_data_with_min_length_max_length_and_extra_attributes() -> None:
    class ValidData(Data):
        MIN_LENGTH: int = 0
        MAX_LENGTH: int = 1
        EXTRA_ATTRIBUTE: str = "EXTRA_ATTRIBUTE"


def test_data_validate_length_with_invalid_length() -> None:
    class ValidData(Data):
        MIN_LENGTH: int = 3
        MAX_LENGTH: int = 5

    assert not ValidData.validate_length("12")
    assert not ValidData.validate_length("123456")


def test_data_validate_length_with_valid_length() -> None:
    class ValidData(Data):
        MIN_LENGTH: int = 3
        MAX_LENGTH: int = 5

    assert ValidData.validate_length("123")
    assert ValidData.validate_length("1234")
    assert ValidData.validate_length("12345")
