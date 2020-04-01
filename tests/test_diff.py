# -*- coding: utf-8 -*-
import pytest
from PIL import Image, ImageDraw


def make_test_image(text="Hello world"):
    img = Image.new('RGB', (100, 30), color=(73, 109, 137))

    d = ImageDraw.Draw(img)
    d.text((10, 10), text, fill=(255, 255, 0))

    return img


def test_diff(image_diff):
    image = make_test_image()
    image_diff(image, image, )


def test_fail_diff(image_diff):
    pytest.raises(AssertionError,
                  image_diff, make_test_image("Foo"), make_test_image("Bar"))


def test_regression(image_regression):
    image = make_test_image()
    image_regression(image)
    image_regression(image)


def test_fail_regression(image_regression):
    image_regression(make_test_image("Foo"))
    pytest.raises(AssertionError,
                  image_regression, make_test_image("Bar"))
