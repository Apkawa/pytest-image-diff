import os
import pathlib
import shutil
import typing
from contextlib import contextmanager
from tempfile import NamedTemporaryFile

from PIL.Image import Image
from _pytest import junitxml
from _pytest.fixtures import FixtureRequest

from pytest_image_diff._types import ImageFileType


def build_filename(
    name: str, suffix: str = "", prefix: str = "", max_length: int = 128
) -> str:
    """
    >>> build_filename("name")
    'name'
    >>> build_filename("name", "suffix", "prefix")
    'prefix-name-suffix'
    >>> build_filename("loooooooong_nameeeeee", "suffix", max_length=20)
    'loooooooo-suffix'
    """
    return "-".join(
        filter(
            None, [prefix, name[: max_length - len(suffix) - len(prefix) - 5], suffix]
        )
    )


@contextmanager
def temp_file(suffix: typing.Optional[str] = None) -> typing.Iterator[pathlib.Path]:
    with NamedTemporaryFile(suffix=suffix, delete=False) as tf:
        temp_image_path = pathlib.Path(tf.name)
    try:
        yield temp_image_path
    finally:
        try:
            tf.close()
            temp_image_path.unlink()
        except FileNotFoundError:
            pass
        except PermissionError:
            # Opps, windows issue
            pass


class TestInfo:
    test_name: str
    class_name: str

    def __init__(self, test_name: str, class_name: str):
        self.test_name = test_name
        self.class_name = class_name

    @staticmethod
    def get_test_info(
        request: FixtureRequest, suffix: str = "", prefix: str = ""
    ) -> "TestInfo":
        try:
            names = junitxml.mangle_testnames(  # type: ignore
                request.node.nodeid.split("::")
            )  #
        except AttributeError:
            # pytest>=2.9.0
            names = junitxml.mangle_test_address(request.node.nodeid)

        classname = ".".join(names[:-1])
        test_name = names[-1]
        return TestInfo(test_name, classname)


def get_test_info(
    request: FixtureRequest, suffix: str = "", prefix: str = ""
) -> TestInfo:
    return TestInfo.get_test_info(request, suffix, prefix)


def image_save(image: ImageFileType, path: typing.Union[str, pathlib.Path]) -> None:
    if isinstance(image, Image):
        image.save(path)
    elif isinstance(image, str):
        if not os.path.exists(image):
            raise ValueError("Image maybe path. Path not exists!")
        shutil.copyfile(image, str(path))
    elif hasattr(image, "read"):
        with open(path, "wb") as f:
            image = typing.cast(typing.BinaryIO, image)
            shutil.copyfileobj(
                image, f
            )  # type: ignore # Workaround for python/mypy#8962
    else:
        raise NotImplementedError()


def ensure_dirs(filepath: str) -> None:
    if not os.path.exists(filepath):
        file_dir = os.path.dirname(filepath)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)


# def pytest_assertrepr_compare(config, op, left, right):
#     print(op, left, right)
#     pass
