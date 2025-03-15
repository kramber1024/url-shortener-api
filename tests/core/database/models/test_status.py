import pytest

from app.core.database.models import Status


@pytest.fixture(scope="module")
def user_id() -> int:
    return 1


@pytest.fixture()
def status() -> Status:
    return Status(user_id=1, active=True)


@pytest.mark.parametrize("user_id", [0, 1, 2])
@pytest.mark.parametrize("active", [True, False])
def test_status_init(user_id: int, active: bool) -> None:
    status: Status = Status(user_id=user_id, active=active)

    assert status._user_id == user_id
    assert status.active == active
    assert status.email_verified is False
    assert status.phone_verified is False


@pytest.mark.parametrize("user_id", [0, 1, 2])
def test_status_property_user_id(user_id: int) -> None:
    status: Status = Status(user_id=user_id, active=True)

    assert status.user_id == user_id


@pytest.mark.parametrize("active", [True, False])
def test_status_property_active(user_id: int, active: bool) -> None:
    status: Status = Status(user_id=user_id, active=active)

    assert status.active == active


@pytest.mark.parametrize("active", [True, False])
def test_status_property_active_setter(active: bool, status: Status) -> None:
    status.active = active

    assert status.active == active


@pytest.mark.parametrize("email_verified", [True, False])
def test_status_property_email_verified(
    email_verified: bool,
    status: Status,
) -> None:
    status.email_verified = email_verified

    assert status.email_verified == email_verified


@pytest.mark.parametrize("phone_verified", [True, False])
def test_status_property_phone_verified(
    phone_verified: bool,
    status: Status,
) -> None:
    status.phone_verified = phone_verified

    assert status.phone_verified == phone_verified


def test_status_repr(status: Status) -> None:
    assert repr(status) == f"<Status {status.user_id}>"
