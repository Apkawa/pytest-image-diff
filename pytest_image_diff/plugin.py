import os
from tempfile import NamedTemporaryFile
from typing import Optional, NamedTuple, Callable

import pytest
from _pytest.fixtures import FixtureRequest

from ._types import ImageFileType, ImageRegressionCallableType, ImageDiffCallableType
from .helpers import get_test_info, build_filename, image_save, ensure_dirs
from .image_diff import _diff


@pytest.fixture(scope='session')
def image_diff_root(request: FixtureRequest) -> str:
    return str(request.config.rootdir)


@pytest.fixture(scope='session')
def image_diff_threshold() -> float:
    return 0.001


@pytest.fixture(scope='session')  # pragma: no cover
def image_diff_dir(image_diff_root: str) -> str:
    """Browser screenshot directory."""
    return os.path.join(image_diff_root, '.tests/image_diff/')


@pytest.fixture(scope='session')
def image_diff_reference_dir(image_diff_root: str) -> str:
    return os.path.join(image_diff_root, 'image_diff_reference')


class DiffInfo(NamedTuple):
    diff_name: str
    image_name: str
    reference_name: str


DiffInfoCallable = Callable[[ImageFileType, str], DiffInfo]


@pytest.fixture(scope="function")
def image_diff_info(
    request: FixtureRequest,
    image_diff_reference_dir: str,
    image_diff_dir: str) -> DiffInfoCallable:
    def _factory(image: ImageFileType, suffix: str = '') -> DiffInfo:
        test_info = get_test_info(request)
        class_name = test_info.class_name
        test_name = test_info.test_name

        reference_dir = os.path.join(image_diff_reference_dir, class_name)
        screenshot_dir = os.path.join(image_diff_dir, class_name)
        reference_name = os.path.join(reference_dir,
                                      build_filename(test_name,
                                                     suffix=suffix + '-reference.png'))
        image_name = os.path.join(screenshot_dir,
                                  build_filename(test_name,
                                                 suffix=suffix + '-screenshot.png'))
        diff_name = os.path.join(screenshot_dir, build_filename(test_name,
                                                                suffix=suffix + '-diff.png'))
        return DiffInfo(
            diff_name=diff_name,
            image_name=image_name,
            reference_name=reference_name,
        )

    return _factory


@pytest.fixture(scope="function")
def image_regression(image_diff_info: DiffInfoCallable,
                     image_diff_threshold: float) -> ImageRegressionCallableType:
    def _factory(image: ImageFileType,
                 threshold: float = image_diff_threshold,
                 suffix: str = '') -> bool:
        diff_info = image_diff_info(image, suffix)
        reference_name = diff_info.reference_name
        diff_name = diff_info.diff_name
        image_name = diff_info.image_name
        if not os.path.exists(reference_name):
            ensure_dirs(reference_name)
            image_save(image, reference_name)
            return True

        ensure_dirs(image_name)
        image_save(image, image_name)
        diff_ratio = _diff(reference_name, image_name, diff_name)
        assert diff_ratio <= threshold, "Image not equals!"

        # Todo clean empty dirs
        for f in [image_name, diff_name]:
            if os.path.exists(f):
                os.unlink(f)
        return True

    return _factory


@pytest.fixture(scope="function")
def image_diff(image_diff_info: DiffInfoCallable,
               image_diff_threshold: float) -> ImageDiffCallableType:
    def _factory(image: ImageFileType,
                 image_2: ImageFileType,
                 threshold: Optional[float] = image_diff_threshold,
                 diff_path: Optional[str] = None,
                 suffix: Optional[str] = '') -> str:
        image_temp_file = NamedTemporaryFile(suffix='.jpg')
        image_2_temp_file = NamedTemporaryFile(suffix='.jpg')
        if not diff_path:
            _info = image_diff_info(image, suffix)
            diff_path = _info.diff_name

        image_save(image, path=image_temp_file.name)
        image_save(image_2, path=image_2_temp_file.name)
        diff_ratio = _diff(image_temp_file.name, image_2_temp_file.name, diff_path)
        assert diff_ratio <= threshold, "Image not equals! See %s" % diff_path
        # Todo clean empty dirs
        for f in [diff_path]:
            if os.path.exists(f):
                os.unlink(f)
        return diff_path

    return _factory
