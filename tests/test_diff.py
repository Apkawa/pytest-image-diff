# -*- coding: utf-8 -*-
import pathlib
import random
import string
import sys
import tempfile
from typing import Union

import pytest
from PIL import Image, ImageDraw

from pytest_image_diff.helpers import image_save


def make_test_image(text="Hello world", size=(100, 30)) -> Image:
    img = Image.new("RGB", size, color=(73, 109, 137))

    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(255, 255, 0))

    return img


@pytest.mark.skipif(sys.platform != "linux", reason="PermissionError in windows")
def test_compare(image_diff):
    image: Union[Image, str, bytes] = make_test_image()
    tf = tempfile.NamedTemporaryFile(suffix=".jpeg")
    # FIXME PermissionError: in windows
    image_save(image, tf.name)
    image2: Union[Image, str, bytes] = pathlib.Path(tf.name)
    image_diff(image, image2)


def test_initial_diff(image_diff, image_diff_dir):
    image = make_test_image()
    suffix = "".join(random.choices(string.ascii_letters, k=10))
    image_diff(image, image, suffix=suffix)


def test_diff(image_diff):
    image = make_test_image()
    image_diff(image, image)


def test_fail_diff(image_diff, image_diff_dir):
    pytest.raises(
        AssertionError, image_diff, make_test_image("Foo"), make_test_image("Bar")
    )


def test_regression(image_regression):
    image = make_test_image()
    image_regression(image)
    image_regression(image)


def test_fail_regression(image_regression):
    image_regression(make_test_image("Foo"))
    pytest.raises(AssertionError, image_regression, make_test_image("Bar"))


def test_fail_regression_different_size(image_regression):
    image_regression(make_test_image("Foo"))
    pytest.raises(
        AssertionError, image_regression, make_test_image("Foo", size=(200, 200))
    )
