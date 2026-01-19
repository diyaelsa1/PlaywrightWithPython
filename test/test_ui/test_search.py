import os

from playwright.sync_api import Page
from playwright.sync_api import Playwright, sync_playwright, expect
from pages.home import HomePage
from pages.results import SearchResultPage
from utils.excel_utils import ExcelUtils
import pytest

excel = ExcelUtils(os.getcwd()+"\\testdata\\twitch_input_data.xlsx")
test_data = excel.get_data_as_list_of_dicts("Sheet1")  # your sheet name

@pytest.mark.parametrize("data", test_data)
def test_streamer_search(page: Page,data)->None:
    url = data["URL"]
    keyword = data["SearchKeyword"]
    print(f"Opening URL: {url}, Searching for: {keyword}")

    home_page = HomePage(page)
    result_page = SearchResultPage(page)
    home_page.load_home_page(url)
    home_page.is_page_loaded()
    home_page.is_search_field_available()
    home_page.search_channel(keyword)
    home_page.is_search_successful(keyword)
    result_page.select_first_visible_streamer_after_scroll(2)
    result_page.is_searched_channel_loaded()