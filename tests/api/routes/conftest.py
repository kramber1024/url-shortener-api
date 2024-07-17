import pytest_asyncio

from app.core.database.models import User
from tests import utils


@pytest_asyncio.fixture(scope="function")
def user_credentials() -> User:
    user: User = User(
        first_name="Humberto",
        last_name="Howell",
        email="Jaclyn.Hirthe@example.org",
        password=utils.DB_USER_PASSWORD,
    )
    user.phone = "+1(234)-567-89-01"
    return user
