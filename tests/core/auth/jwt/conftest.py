import datetime

import pytest


@pytest.fixture
def current_time() -> int:
    return int(datetime.datetime.now(datetime.UTC).timestamp())
