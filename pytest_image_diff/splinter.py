import os
from typing import Optional, Generator

import pytest
from typing_extensions import Protocol

from .helpers import temp_file

try:
    # Check pytest-splinter
    from pytest_splinter.plugin import Browser
except ImportError:
    Browser = None

if Browser:
    from ._types import ImageRegressionCallableType

    class ScreenshotRegressionCallableType(Protocol):
        def __call__(
            self,
            browser: Optional[Browser] = None,
            threshold: Optional[float] = None,
            suffix: Optional[str] = None,
            xpath: Optional[str] = "",
        ) -> bool:
            pass

    __all__ = ["screenshot_regression"]

    @pytest.fixture(scope="function")
    def screenshot_regression(
        browser: Browser,
        image_regression: ImageRegressionCallableType,
        image_diff_threshold: float,
    ) -> Generator[ScreenshotRegressionCallableType, None, None]:
        """
        Check regression browser screenshot

        :param browser: optional, by default from `browser` fixture
        :param threshold: float, by default from `image_diff_threshold`
        :param suffix: str, need for multiple checks  by one test
        :param xpath: str, optional xpath expression to select an element to
                screenshot instead of page
        """
        default_browser = browser

        def _factory(
            browser: Optional[Browser] = None,
            threshold: Optional[float] = None,
            suffix: Optional[str] = "",
            xpath: Optional[str] = "",
        ) -> bool:
            if browser is None:
                browser = default_browser

            if threshold is None:
                threshold = image_diff_threshold

            with temp_file(suffix=".png") as temp_image_path:
                screenshot_path = os.fspath(temp_image_path)

                if xpath:
                    # `unique_file=False` since we already have a temporary file
                    #
                    # Since an xpath screenshot composes its own file name,
                    # we need to give it the prefix and
                    # suffix as separate parameters. `:-4` for the path without extension,
                    # then suffix given manually.
                    browser.find_by_xpath(xpath).first.screenshot(
                        screenshot_path[:-4],
                        suffix=screenshot_path[-4:],
                        unique_file=False,
                        full=True,
                    )
                else:
                    browser.driver.save_screenshot(screenshot_path)

                result = image_regression(screenshot_path, threshold, suffix)
                return result

        yield _factory
