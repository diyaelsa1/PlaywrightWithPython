from playwright.sync_api import sync_playwright


def test_api_page_load():
    with sync_playwright() as p:
        request = p.request.new_context()
        response=request.get("https://m.twitch.tv/directory")
        print(response.status)
        print(response.text)
        assert response.status == 200
        request.dispose()



