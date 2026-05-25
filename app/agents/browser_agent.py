from playwright.sync_api import sync_playwright

class BrowserAgent:

    @staticmethod
    def search(query: str):

        with sync_playwright() as p:

            browser = p.chromium.launch()

            page = browser.new_page()

            page.goto(
                f"https://www.google.com/search?q={query}"
            )

            content = page.content()

            browser.close()

            return content