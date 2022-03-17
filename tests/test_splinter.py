import os
import tempfile

import pytest

try:
    import pytest_splinter
except ImportError:
    pytest_splinter = None

with_splinter = pytest.mark.skipif(
    pytest_splinter is None, reason="pytest-splinter not installed"
)


@pytest.fixture(scope="session")
def splinter_headless():
    return True


@pytest.fixture(scope="session")
def splinter_webdriver(request):
    return request.config.option.splinter_webdriver or "chrome"


@pytest.fixture(scope="session")
def splinter_webdriver_executable(request, splinter_webdriver):
    """Webdriver executable directory."""
    executable = request.config.option.splinter_webdriver_executable
    if not executable and splinter_webdriver == "chrome":
        from chromedriver_binary import chromedriver_filename

        executable = chromedriver_filename
    return os.path.abspath(executable) if executable else None


@with_splinter
def test_splinter_fixture(screenshot_regression):
    assert screenshot_regression


@with_splinter
def test_splinter(browser, screenshot_regression):
    tf = tempfile.NamedTemporaryFile(suffix=".html")
    tf.write(b"<html><body><h1>Example</h1></body></html>")
    tf.flush()

    browser.driver.set_window_size(1280, 1024)
    browser.visit("file://" + tf.name)
    screenshot_regression()
    browser.driver.set_window_size(800, 600)
    screenshot_regression(suffix="small_window")


@with_splinter
def test_splinter_with_xpath(browser, screenshot_regression):
    tf = tempfile.NamedTemporaryFile(suffix=".html")
    tf.write(b"<html><body><h1>Example</h1></body></html>")
    tf.flush()

    browser.driver.set_window_size(1280, 1024)
    browser.visit("file://" + tf.name)
    screenshot_regression(xpath="//h1")
