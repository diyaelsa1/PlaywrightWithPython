import threading
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright


class PlaywrightFactory:

    def __init__(self, headless: bool = False):
        self._headless = headless

        self._tl_browser = threading.local()
        self._tl_context = threading.local()
        self._tl_page = threading.local()
        self._tl_playwright = threading.local()

    def get_playwright(self) -> Playwright | None:
        return getattr(self._tl_playwright, "value", None)

    def get_browser(self) -> Browser | None:
        return getattr(self._tl_browser, "value", None)

    def get_context(self) -> BrowserContext | None:
        return getattr(self._tl_context, "value", None)

    def get_page(self) -> Page | None:
        return getattr(self._tl_page, "value", None)

    def initialise_browser(
        self,
        browser_name: str,
        device_name: str | None = None,
        locale: str | None = None,
        color_scheme: str | None = None,
    ) -> Page:
        """Initializes browser, context and page for desktop or mobile device."""

        self._tl_playwright.value = sync_playwright().start()
        pw = self.get_playwright()

        if browser_name.lower() == "chromium":
            self._tl_browser.value = pw.chromium.launch(headless=self._headless)
        elif browser_name.lower() == "firefox":
            self._tl_browser.value = pw.firefox.launch(headless=self._headless)
        elif browser_name.lower() in ["webkit", "safari"]:
            self._tl_browser.value = pw.webkit.launch(headless=self._headless)
        elif browser_name.lower() == "chrome":
            self._tl_browser.value = pw.chromium.launch(
                headless=self._headless, channel="chrome"
            )
        elif browser_name.lower() == "edge":
            self._tl_browser.value = pw.chromium.launch(
                headless=self._headless, channel="msedge"
            )
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        # Context options
        context_options = {}

        if device_name:
            device = pw.devices.get(device_name)
            if not device:
                raise ValueError(f"Unsupported device: {device_name}")
            context_options.update(device)

        if locale:
            context_options["locale"] = locale

        if color_scheme:
            context_options["color_scheme"] = color_scheme

        self._tl_context.value = self.get_browser().new_context(**context_options)
        self._tl_page.value = self.get_context().new_page()

        return self.get_page()

    def cleanup(self):
        """Close page, context, browser, and stop Playwright."""
        if self.get_page():
            self.get_page().close()
            self._tl_page.value = None

        if self.get_context():
            self.get_context().close()
            self._tl_context.value = None

        if self.get_browser():
            self.get_browser().close()
            self._tl_browser.value = None

        if self.get_playwright():
            self.get_playwright().stop()
            self._tl_playwright.value = None
