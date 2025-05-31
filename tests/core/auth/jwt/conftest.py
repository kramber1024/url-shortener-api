import time

import pytest


@pytest.fixture()
def current_time() -> int:
    return int(time.time())
