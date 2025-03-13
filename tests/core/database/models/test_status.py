import pytest

from app.core.database.models import Status


@pytest.fixture()
def user_id() -> int:
    return 1


def test_status_init(user_id: int) -> None:
    active: bool = True

    status: Status = Status(user_id=user_id, active=active)

    assert status.user_id == user_id
    assert status.active == active
    assert not status.email_verified
    assert not status.phone_verified


@pytest.mark.parametrize("user_id", [41421987421987, 14942109, 0, -1, 8484])
def test_status_property_user_id(user_id: int) -> None:
    status: Status = Status(user_id=user_id)

    assert status.user_id == user_id


def test_status_property_active(user_id: int) -> None:
    active: bool = True

    status: Status = Status(user_id=user_id, active=active)

    assert status.active == active


def test_status_property_active_valid(user_id: int) -> None:
    active: bool = False
    status: Status = Status(user_id=user_id, active=not active)

    status.active = active

    assert status.active == active


def test_status_property_email_verified(user_id: int) -> None:
    status: Status = Status(user_id=user_id)

    assert not status.email_verified


def test_status_property_email_verified_valid(user_id: int) -> None:
    email_verified: bool = True
    status: Status = Status(user_id=user_id)

    status.email_verified = email_verified

    assert status.email_verified == email_verified


def test_status_property_phone_verified(user_id: int) -> None:
    status: Status = Status(user_id=user_id)

    assert not status.phone_verified


def test_status_property_phone_verified_valid(user_id: int) -> None:
    phone_verified: bool = True
    status: Status = Status(user_id=user_id)

    status.phone_verified = phone_verified

    assert status.phone_verified == phone_verified
