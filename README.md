[![PyPi](https://img.shields.io/pypi/v/pytest-image-diff.svg)](https://pypi.python.org/pypi/pytest-image-diff)
[![ci](https://github.com/Apkawa/pytest-image-diff/actions/workflows/ci.yml/badge.svg)](https://github.com/Apkawa/pytest-image-diff/actions/workflows/ci.yml)
[![Documentation Status](https://readthedocs.org/projects/pytest-image-diff/badge/?version=latest)](https://pytest-image-diff.readthedocs.io/en/latest/?badge=latest)
[![Codecov](https://codecov.io/gh/Apkawa/pytest-image-diff/branch/master/graph/badge.svg)](https://codecov.io/gh/Apkawa/pytest-image-diff)
[![PyPi Python versions](https://img.shields.io/pypi/pyversions/pytest-image-diff.svg)](https://pypi.python.org/pypi/pytest-image-diff)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

# pytest-image-diff

# Installation

```bash
pip install pytest-image-diff
```

or from git

```bash
pip install -e git+https://githib.com/Apkawa/pytest-image-diff.git@master#egg=pytest-image-diff
```

Python>=3.6


# Usage

```python
from typing import Union
from PIL import Image


def test_compare(image_diff):
    image: Image or str or bytes = Image.new()
    image2: Image or str or bytes = '/path/to/image.jpeg'
    image_diff(image, image2)


def test_regression(image_regression):
    image: Union[Image, str, bytes] = Image.new()
    image_regression(image, threshold=0.5)
```

Also use with assert

```python
import pytest

from typing import Union
from PIL import Image

@pytest.fixture(scope="session")
def image_diff_throw_exception() -> bool:
    """
    Set default throw exception. By default - True
    """
    return False

def test_compare(image_diff):
    image: Image or str or bytes = Image.new()
    image2: Image or str or bytes = '/path/to/image.jpeg'
    assert image_diff(image, image2)
    assert image_diff(image, image2, threshold=0.5)
    # Also can check threshold in compare, ie
    assert image_diff(image, image2) < 0.5
    # For different checks in one test
    assert image_diff(image, image2, threshold=0.5, suffix="one")
    # Or without fixture image_diff_throw_exception
    assert image_diff(image, image2, threshold=0.5, throw_exception=False)


def test_regression(image_regression):
    image: Union[Image, str, bytes] = Image.new()
    assert image_regression(image, threshold=0.5)
    # Also can check threshold in compare, ie
    assert image_regression(image) < 0.5
    # For different checks in one test
    assert image_regression(image, threshold=0.5, suffix="foo")
    # Or without fixture image_diff_throw_exception
    assert image_regression(image, threshold=0.5, throw_exception=False)
```

First run creates reference images

## pytest-splinter

Fixture `screenshot_regression` enabled if pytest-splinter installed

```python3
import pytest

@pytest.fixture
def admin_browser(request, browser_instance_getter):
    """Admin browser fixture."""
    # browser_instance_getter function receives parent fixture -- our admin_browser
    return browser_instance_getter(request, admin_browser)

def test_2_browsers(browser, admin_browser, screenshot_regression):
    """Test using 2 browsers at the same time."""
    browser.visit('http://google.com')
    admin_browser.visit('http://admin.example.com')

    screenshot_regression(suffix="browser")
    screenshot_regression(admin_browser, suffix="admin browser")

def test_pytest_splinter(browser, screenshot_regression):
    # Recommend fix window size for avoid regression
    browser.driver.set_window_size(1280, 1024)

    browser.visit('http://google.com')

    screenshot_regression(suffix="main")
    # ... some interaction
    browser.click()
    screenshot_regression(suffix="success")
    # you can use xpath expression for part of page
    screenshot_regression(xpath="//h1")
```
