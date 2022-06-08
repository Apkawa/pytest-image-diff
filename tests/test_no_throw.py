# -*- coding: utf-8 -*-
import os
import random
import shutil
import string

import pytest
from PIL import Image, ImageDraw


def make_test_image(text="Hello world", size=(100, 30)) -> Image:
    img = Image.new("RGB", size, color=(73, 109, 137))

    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(255, 255, 0))

    return img


@pytest.fixture(scope="session")
def image_diff_throw_exception() -> bool:
    """
    Set default throw exception. By default - True
    """
    return False


def test_initial_diff(image_diff, image_diff_dir):
    suffix = "".join(random.choices(string.ascii_letters, k=10))
    image = make_test_image()
    assert image_diff(image, image, suffix=suffix)


def test_diff(image_diff):
    image = make_test_image()
    assert image_diff(image, image)


def test_fail_diff(image_diff, image_diff_dir):
    assert not image_diff(make_test_image("Foo"), make_test_image("Bar"))
    assert image_diff(make_test_image("Foo"), make_test_image("Bar")) > 0


def test_regression(image_regression):
    image = make_test_image()
    assert image_regression(image)
    assert image_regression(image)


def test_fail_regression(image_regression):
    assert image_regression(make_test_image("Foo"))
    assert not image_regression(make_test_image("Bar"))
    assert image_regression(make_test_image("Baz")) > 0


def test_fail_regression_different_size(image_regression):
    assert image_regression(make_test_image("Foo"))
    assert not image_regression(make_test_image("Foo", size=(200, 200)))
