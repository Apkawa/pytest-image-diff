import pytest
from tempfile import NamedTemporaryFile
from typing import Optional, Generator
from typing_extensions import Protocol


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
        """
        default_browser = browser

        def _factory(
            browser: Optional[Browser] = None,
            threshold: Optional[float] = None,
            suffix: Optional[str] = "",
        ) -> bool:
            if browser is None:
                browser = default_browser

            if threshold is None:
                threshold = image_diff_threshold
            tf = NamedTemporaryFile(suffix=".png")
            image = tf.name
            browser.driver.save_screenshot(image)
            return image_regression(image, threshold, suffix)

        yield _factory
