import os
import pathlib

import pytest
from _pytest.fixtures import FixtureRequest

from pytest_image_diff._types import PathType


@pytest.fixture(scope="session")
def image_diff_root(request: FixtureRequest) -> PathType:
    """
    Root path for storing diff images. By default - `request.config.rootdir`
    """
    return os.path.join(request.config.rootdir, "tests")  # type: ignore


@pytest.fixture(scope="session")
def image_diff_dir(image_diff_root: str) -> PathType:
    """
    Path for store diff images. by default - '{image_diff_root}.tests/image_diff/'
    """
    return pathlib.Path(image_diff_root) / ".tests" / "image_diff"
