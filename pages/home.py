import re
from playwright.sync_api import Page,expect
from utils.helpers import CommonFunctions


class HomePage():

    def __init__(self, page: Page):
        self.page = page
        self.timeout = 15000
        self.cf = CommonFunctions(page)
        self.search_input=page.get_by_placeholder("Search")
        self.search_text_label=page.get_by_role("heading", name=re.compile("People searching for \"",re.IGNORECASE))

    def load_home_page(self,url):
        """Navigates to Twitch home page and handles initial pop-ups."""
        self.page.goto(url)
        self.cf.wait_for_page_ready()
        self.cf.close_modal_if_present()

    def is_page_loaded(self):
        expect(self.search_input).to_be_visible()

    def search_channel(self, text):
        """Searches for the given text using Twitch search."""
        self.search_input.fill(text)
        expect( self.page.get_by_role("link", name="StarCraft II StarCraft II")).to_be_visible()
        self.page.get_by_role("link", name="StarCraft II StarCraft II").click()
        self.cf.wait_for_page_ready()
        expect(self.page.get_by_role("heading", name="StarCraft II")).to_be_visible()

    def is_search_successful(self,text):
        search_label = self.get_search_text_label(text)
        expect(search_label).to_be_visible()
        #expect(self.search_text_label).to_be_visible()

    def is_search_field_available(self):
        self.search_input.wait_for(state="visible", timeout=self.timeout)
        self.search_input.scroll_into_view_if_needed()
        expect(self.search_input).to_be_visible()

    def get_search_text_label(self, search_term: str):
        return self.page.get_by_role(
            "heading",
            name=re.compile(search_term, re.IGNORECASE)
        )
