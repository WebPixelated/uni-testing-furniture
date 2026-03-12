import allure
from playwright.sync_api import Page, Locator, expect
from utils.logger import logger


class BasePage:
    BASE_URL = "https://mebelmart-saratov.ru"

    def __init__(self, page: Page):
        self.page = page

    # Navigation

    def open(self, url_path: str = ""):
        """Navigate to url_path relative to BASE_URL."""
        full_url = f"{self.BASE_URL}{url_path}"
        logger.info(f"Opening: {full_url}")
        with allure.step(f"Open URL: {full_url}"):
            self.page.goto(full_url)
            self.page.wait_for_load_state("domcontentloaded")

    # Element access

    def find(self, locator: str) -> Locator:
        """Return a Locator for the given XPath / CSS Selector."""
        return self.page.locator(locator)

    def find_first(self, locator: str) -> Locator:
        """Return the first matching element."""
        return self.page.locator(locator).first

    # Actions

    def click(self, locator: str):
        logger.debug(f"Click: {locator}")
        self.find(locator).click()

    def input_text(self, locator: str, text: str):
        logger.debug(f"Input '{text}' -> {locator}")
        el = self.find(locator)
        el.click()
        el.fill(text)

    def get_text(self, locator: str) -> str:
        text = self.find(locator).inner_text().strip()
        logger.debug(f"Got text '{text}' from {locator}")
        return text

    # Waits

    def wait_for_element(self, locator: str, timeout: int = 10_000):
        """Wait until element is visible."""
        logger.debug(f"Waiting for: {locator}")
        self.find(locator).wait_for(state="visible", timeout=timeout)

    def wait_for_network_idle(self):
        self.page.wait_for_load_state("networkidle")

    # Assertions

    def assert_visible(self, locator: str, timeout: int = 10_000):
        expect(self.find(locator)).to_be_visible(timeout=timeout)

    def assert_text_contains(self, locator: str, text: str, timeout: int = 10_000):
        expect(self.find(locator)).to_contain_text(text, timeout=timeout)
