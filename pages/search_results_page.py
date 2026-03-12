import allure
from pages.base_page import BasePage
from utils.logger import logger


class SearchResultsPage(BasePage):
    # --- LOCATORS ---
    # Same product-card pattern used in the catalog
    PRODUCT_CARD = (
        "//div[contains(@class, 'product-card') "
        "and not(contains(@class, 'product-card__'))]"
    )
    CARD_TITLE_LINK = "//div[contains(@class, 'product-card__name')]//a"

    # Heading or notification when no results are found
    NO_RESULTS = (
        "//*[contains(text(), 'ничего не найдено') or contains(text(), 'не найдено')]"
    )

    # --- PUBLIC API ---

    @allure.step("Wait for search results to appear")
    def wait_for_results(self, timeout: int = 10_000):
        self.find(self.PRODUCT_CARD).first.wait_for(state="visible", timeout=timeout)

    @allure.step("Get name of the first search result")
    def get_first_product_name(self) -> str:
        first_card = self.find(self.PRODUCT_CARD).first
        name = first_card.locator(self.CARD_TITLE_LINK).inner_text().strip()
        logger.info(f"First search result: '{name}'")
        return name

    @allure.step("Get all product names from search results")
    def get_all_product_names(self) -> list[str]:
        cards = self.find(self.PRODUCT_CARD)
        names = [
            cards.nth(i).locator(self.CARD_TITLE_LINK).inner_text().strip()
            for i in range(cards.count())
        ]
        logger.info(f"Search result names: {names}")
        return names

    def has_no_results(self) -> bool:
        try:
            return self.find(self.NO_RESULTS).is_visible(timeout=5_000)
        except Exception:
            return False
