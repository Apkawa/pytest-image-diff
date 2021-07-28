import os

import pytest
from _pytest.fixtures import FixtureRequest


@pytest.fixture(scope="session")
def image_diff_root(request: FixtureRequest) -> str:
    """
    Root path for storing diff images. By default - `request.config.rootdir`
    """
    return os.path.join(request.config.rootdir, "tests")
