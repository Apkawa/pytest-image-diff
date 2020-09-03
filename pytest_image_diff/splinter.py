from tempfile import NamedTemporaryFile
from typing import Optional

import pytest

try:
    # Check pytest-splinter
    from pytest_splinter.plugin import Browser
except ImportError:
    raise

from ._types import ScreenshotRegressionCallableType, ImageRegressionCallableType

__all__ = ['screenshot_regression']


@pytest.fixture(scope="function")
def screenshot_regression(
    browser: Browser,
    image_regression: ImageRegressionCallableType,
    image_diff_threshold: float
) -> ScreenshotRegressionCallableType:
    """
    Check regression browser screenshot
    :param threshold: float, by default from `image_diff_threshold`
    :param suffix: str, need for multiple checks  by one test
    """

    def _factory(threshold: float = image_diff_threshold,
                 suffix: Optional[str] = '') -> bool:
        tf = NamedTemporaryFile(suffix='.png')
        image = tf.name
        browser.driver.save_screenshot(image)
        return image_regression(image, threshold, suffix)

    return _factory
