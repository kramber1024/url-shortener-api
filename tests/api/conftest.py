import pytest_asyncio

from app.core.database.models import User
from tests import utils


@pytest_asyncio.fixture(scope="function")
def user_credentials() -> User:
    user: User = User(
        first_name="Freddie",
        last_name="Bosco",
        email="Freddie.Bosco@example.com",
        password=utils.DB_USER_PASSWORD,
    )
    user.id = 1234567890123456789
    user.phone = "+1(234)-567-89-01"
    return user
