import allure
from pages.base_page import BasePage
from utils.logger import logger


class FavoritePage(BasePage):
    URL = "/favorite/"

    # --- LOCATORS ---
    # Product card inside the favorites container
    PRODUCT_CARD = (
        "//div[contains(@class, 'product-card') "
        "and not(contains(@class, 'product-card__'))]"
    )

    # Relative locators (used with .locator() on a card)
    CARD_TITLE_LINK = "//div[contains(@class, 'product-card__name')]//a"
    CARD_CURRENT_PRICE = "//div[contains(@class, 'product-card__now_price')]/span/b"
    CARD_FAV_BTN = "//div[contains(@class, 'product-card__favorites')]//a"
    CARD_REMOVE_BTN = "//div[contains(@class, 'product-card__favorite-delete')]"
    EMPTY_FAVORITES = (
        "//div[contains(normalize-space(text()), 'В избранном пока еще ничего нет')]"
    )

    # --- PUBLIC API ---
    def open_favorites(self):
        with allure.step("Open favorites page"):
            super().open(self.URL)

    @allure.step("Wait for favorites products to load")
    def wait_for_products_to_load(self, timeout: int = 10_000):
        self.find(self.PRODUCT_CARD).first.wait_for(state="visible", timeout=timeout)

    @allure.step("Get all product names in favorites")
    def get_all_product_names(self) -> list[str]:
        cards = self.find(self.PRODUCT_CARD)
        names = []
        count = cards.count()
        for i in range(count):
            name = cards.nth(i).locator(self.CARD_TITLE_LINK).inner_text().strip()
            names.append(name)
        logger.info(f"Favorites: {names}")
        return names

    @allure.step("Check if '{product_name}' is in favorites")
    def is_product_in_favorites(self, product_name: str) -> bool:
        names = self.get_all_product_names()
        found = any(product_name.lower() in n.lower() for n in names)
        logger.info(f"Product '{product_name}' {'found' if found else 'NOT found'}")
        return found

    @allure.step("Check if '{product_href}' is in favorites by href")
    def is_product_in_favorites_by_href(self, product_href: str) -> bool:
        cards = self.find(self.PRODUCT_CARD)
        count = cards.count()
        for i in range(count):
            href = cards.nth(i).locator(self.CARD_TITLE_LINK).get_attribute("href")
            if href == product_href:
                logger.info(f"Product with href '{product_href}' found in favorites")
                return True
        logger.info(f"Product with href '{product_href}' NOT found in favorites")
        return False

    @allure.step("Get count of favorites")
    def get_favorites_count(self) -> int:
        return self.find(self.PRODUCT_CARD).count()
