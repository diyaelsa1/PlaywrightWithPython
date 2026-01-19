#TO DEFINE ALL REUSABLE FUNCTIONS REQUIRED FOR TEST AUTOMATION
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import Page
from pathlib import Path
import threading
import base64

class CommonFunctions:

    def __init__(self, page:Page):
        self.page = page
        self.model_selectors = [
            "button:has-text('Accept')",
            "button:has-text('Got it')",
            "button:has-text('Close')"
        ]
        self.timeout=8000

    def wait_for_page_ready(self) -> None:
        """
        Waits until the page has finished network activity.
        """
        self.page.wait_for_load_state("domcontentloaded", timeout=self.timeout)

    def scroll_down_with_mouse(self,selector, times: int = 2, pause_ms: int = 3000) -> None:
        """
        Scrolls down the page a specified number of times using mouse wheel.

        Args:
            times (int): Number of scroll actions.
            pause_ms (int): Pause between scrolls in milliseconds.
        """
        self.page.get_by_role("list").hover()
        for _ in range(times):
            self.page.mouse.wheel(0, 1000)
            self.page.wait_for_timeout(pause_ms)


    def scroll_down_with_js(self, times: int = 2, pause_ms: int = 3000) -> None:
        list_element = self.page.get_by_role("list")

        for _ in range(5):  # 5 scroll steps
            list_element.evaluate("el => el.scrollBy(0, 300)")
            self.page.wait_for_timeout(self.timeout)  # wait for lazy load


    def scroll_down_with_keys(self,times: int = 2)-> None:
        """
        Scrolls down the page a specified number of times.

        Args:
            times (int): Number of scroll actions.
        """
        for _ in range(times):
            self.page.keyboard.press("ArrowDown")
            self.page.wait_for_timeout(self.timeout)

    def close_modal_if_present(self) -> None:
        """
        Closes common modal dialogs if they appear on the page.
        """
        try:
            for selector in self.model_selectors:
                locator = self.page.locator(selector)
                if locator.count() > 0 and locator.first.is_visible():
                    try:
                        locator.first.click(timeout=3000)
                        return
                    except PlaywrightTimeoutError:
                        pass
        except:
            pass


    def take_screenshot(self) -> str:
        screenshot_dir = Path("./screenshot")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        path = screenshot_dir / f"{threading.get_ident()}.png"
        buffer = self.page.screenshot(path=path, full_page=True)
        return base64.b64encode(buffer).decode("utf-8")