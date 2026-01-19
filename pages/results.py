import re
from utils.helpers import CommonFunctions
from playwright.sync_api import Page,expect

class SearchResultPage:

    def __init__(self, page:Page):
        self.page = page
        self.cf = CommonFunctions(page)
        self.streamer_card_button = page.get_by_role("button", name=re.compile(r"Live \d+ viewers"))
        self.loaded_channel_follow_button=page.locator("div").filter(has_text="Follow").nth(4)
        self.loaded_channel_metadata_Section=page.get_by_role("button", name="Open channel metadata for")
        self.scroll_container= '[data-a-target="root-scroller"]'
        self.video_locator = self.page.locator('[data-a-target="video-ref"]')

    def select_first_visible_streamer_after_scroll(self, scroll_times: int) -> None:
        """
        Scrolls the search results page a fixed number of times and selects
        the first visible streamer card.

        Args:
            scroll_times (int): Number of vertical scroll actions to perform
                                before selecting a streamer. Default is 2.

        Returns:
            None

        Raises:
            Exception: If no visible streamer card is found after scrolling.
        """
        self.cf.scroll_down_with_mouse(self.scroll_container,times=scroll_times)
        cards = self.streamer_card_button.count()
        for i in range(cards):
            card =  self.streamer_card_button.nth(i)
            if card.is_visible():
                card.click()
                self.cf.wait_for_page_ready()
                return

        raise Exception("No visible streamer found after scrolling")

    def is_searched_channel_loaded(self):
        self.verify_playback()
        expect(self.loaded_channel_metadata_Section).to_be_visible()
        self.cf.take_screenshot()

    def verify_playback(self):
        video = self.page.locator("div.iczchi > video")
        # wait for element to exist
        video.wait_for(state="attached", timeout=30000)
        # wait until video is playable
        self.page.wait_for_function("() => document.querySelector('div.iczchi > video')?.readyState > 0",timeout=60000)
        print("Mobile Twitch video is ready to play")