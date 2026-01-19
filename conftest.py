import pytest
from factory.playwright_factory import PlaywrightFactory

@pytest.fixture(scope="function")
def page():
    """
    All tests run on:
    - Real Google Chrome
    - Mobile emulator (Pixel 7)
    """

    factory = PlaywrightFactory(headless=False)

    page = factory.initialise_browser(
        browser_name="chrome",
        device_name="Pixel 7",       # Mobile emulation
        locale="en-US",
        color_scheme="dark"
    )

    yield page

    factory.cleanup()