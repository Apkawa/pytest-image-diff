import os
from typing import Optional, NamedTuple, cast, Callable, Generator, Union

import pytest
from _pytest.fixtures import FixtureRequest
from _pytest.python import Function
from _pytest.runner import CallInfo

from ._types import ImageFileType, ImageRegressionCallableType, ImageDiffCallableType
from .helpers import get_test_info, build_filename, image_save, ensure_dirs, temp_file
from .image_diff import _diff

try:
    from .splinter import screenshot_regression  # noqa
except ImportError:
    pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)  # type: ignore
def pytest_runtest_makereport(item: Function, call: CallInfo):  # type: ignore
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # set a report attribute for each phase of a call, which can
    # be "setup", "call", "teardown"

    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture(scope="session")
def image_diff_threshold() -> float:
    """
    Set default threshold differences of images. By default - 0.001
    """
    return 0.001


@pytest.fixture(scope="session")
def image_diff_throw_exception() -> bool:
    """
    Set default throw exception. By default - True
    """
    return True


@pytest.fixture(scope="session")
def image_diff_root(request: FixtureRequest) -> str:
    """
    Root path for storing diff images. By default - `request.config.rootdir`
    """
    return str(request.config.rootdir)  # type: ignore


@pytest.fixture(scope="session")  # pragma: no cover
def image_diff_dir(image_diff_root: str) -> str:
    """
    Path for store diff images. by default - '{image_diff_root}.tests/image_diff/'
    """
    return os.path.join(image_diff_root, ".tests/image_diff/")


@pytest.fixture(scope="session")
def image_diff_reference_dir(image_diff_root: str) -> str:
    """
    Path for store reference images
    """
    return os.path.join(image_diff_root, "image_diff_reference")


class DiffInfo(NamedTuple):
    diff_name: str
    image_name: str
    reference_name: str


DiffInfoCallableType = Callable[[ImageFileType, Optional[str]], DiffInfo]


class DiffCompareResult:
    value: float
    thresh: float
    diff_path: Optional[str]

    CompareType = Union[int, float, "DiffCompareResult"]

    def __init__(self, value: float, thresh: float, diff_path: Optional[str] = None):
        self.value = value
        self.thresh = thresh
        self.diff_path = diff_path

    def __repr__(self) -> str:
        return f"diff: {round(self.value, 4)}; thresh: {self.thresh}; diff path: {self.diff_path}"

    def __bool__(self) -> bool:
        return self.value <= self.thresh

    def __gt__(self, other: CompareType) -> bool:
        return self.value > other

    def __ge__(self, other: CompareType) -> bool:
        return self.value >= other

    def __lt__(self, other: CompareType) -> bool:
        return self.value < other

    def __le__(self, other: CompareType) -> bool:
        return self.value <= other


@pytest.fixture(scope="function")
def _image_diff_info(
    request: FixtureRequest, image_diff_reference_dir: str, image_diff_dir: str
) -> DiffInfoCallableType:
    """
    For internal use
    """

    def _factory(image: ImageFileType, suffix: Optional[str] = None) -> DiffInfo:
        test_info = get_test_info(request)
        class_name = test_info.class_name
        test_name = test_info.test_name
        if suffix is None:
            # Todo enumerate every call
            suffix = ""

        reference_dir = os.path.join(image_diff_reference_dir, class_name)
        screenshot_dir = os.path.join(image_diff_dir, class_name)
        reference_name = os.path.join(
            reference_dir, build_filename(test_name, suffix=suffix + "-reference.png")
        )
        image_name = os.path.join(
            screenshot_dir, build_filename(test_name, suffix=suffix + "-screenshot.png")
        )
        diff_name = os.path.join(
            screenshot_dir, build_filename(test_name, suffix=suffix + "-diff.png")
        )
        return DiffInfo(
            diff_name=diff_name, image_name=image_name, reference_name=reference_name
        )

    return _factory


@pytest.fixture(scope="function")
def image_regression(
    request: FixtureRequest,
    _image_diff_info: DiffInfoCallableType,
    image_diff_threshold: float,
    image_diff_throw_exception: bool,
) -> Generator[ImageRegressionCallableType, None, None]:
    """
    Check regression image.

    :param image: `PIL.Image` or `PathLike` or `io.BinaryIO`
    :param threshold: float, by default from `image_diff_threshold`
    :param suffix: str, need for multiple checks  by one test
    :return: bool
    """

    def _factory(
        image: ImageFileType,
        threshold: Optional[float] = None,
        suffix: Optional[str] = None,
        throw_exception: Optional[bool] = None,
    ) -> "DiffCompareResult":
        if threshold is None:
            threshold = image_diff_threshold
        if throw_exception is None:
            throw_exception = image_diff_throw_exception
        diff_info = _image_diff_info(image, suffix)
        reference_name = diff_info.reference_name
        diff_name = diff_info.diff_name
        image_name = diff_info.image_name
        if not os.path.exists(reference_name):
            ensure_dirs(reference_name)
            image_save(image, reference_name)
            return DiffCompareResult(0, threshold)

        def _cleanup() -> None:
            if request.node.rep_setup.passed and request.node.rep_call.failed:
                # Do not cleanup regression artifacts
                return
            for f in [image_name, diff_name]:
                if os.path.exists(f):
                    try:
                        os.unlink(f)
                    except PermissionError:
                        # Opps, have windows issue
                        pass

        request.addfinalizer(_cleanup)

        ensure_dirs(diff_name)
        ensure_dirs(image_name)
        image_save(image, image_name)
        diff_ratio = _diff(reference_name, image_name, diff_name)
        cond = DiffCompareResult(diff_ratio, threshold, diff_name)
        if throw_exception:
            assert cond, "Image not equals!"  # noqa
        return cond

    yield _factory


@pytest.fixture(scope="function")
def image_diff(
    request: FixtureRequest,
    _image_diff_info: DiffInfoCallableType,
    image_diff_threshold: float,
    image_diff_throw_exception: bool,
) -> Generator[ImageDiffCallableType, None, None]:
    """
    Compare two image

    :param image: `PIL.Image` or `PathLike` or `io.BinaryIO`
    :param image2: `PIL.Image` or `PathLike` or `io.BinaryIO`
    :param threshold: float, by default from `image_diff_threshold`
    :param suffix: str, need for multiple checks  by one test
    :return: bool
    """

    def _factory(
        image: ImageFileType,
        image_2: ImageFileType,
        threshold: Optional[float] = None,
        suffix: Optional[str] = None,
        throw_exception: Optional[bool] = None,
    ) -> DiffCompareResult:
        if threshold is None:
            threshold = image_diff_threshold
        if throw_exception is None:
            throw_exception = image_diff_throw_exception

        _info = _image_diff_info(image, suffix)
        diff_path = cast(str, _info.diff_name)

        ensure_dirs(diff_path)

        def _cleanup() -> None:
            if request.node.rep_setup.passed and request.node.rep_call.failed:
                # Do not cleanup regression artifacts
                return
            for f in [diff_path]:
                if os.path.exists(f):
                    os.unlink(f)

        request.addfinalizer(_cleanup)

        with temp_file(suffix=".jpg") as image_temp_file, temp_file(
            suffix=".jpg"
        ) as image_2_temp_file:
            image_save(image, path=image_temp_file)
            image_save(image_2, path=image_2_temp_file)
            diff_ratio = _diff(image_temp_file, image_2_temp_file, diff_path)
        cond = DiffCompareResult(diff_ratio, threshold, diff_path)
        if throw_exception:
            assert cond, "Image not equals! See %s" % diff_path  # noqa
        return cond

    yield _factory
