import allure
from pages.base_page import BasePage
from utils.logger import logger


class CartPage(BasePage):
    URL = "/cart"

    # --- LOCATORS ---
    # Each item row in the cart
    CART_ITEM = "//div[contains(@class, 'list-group-item')]"

    # Within an item row (relative)
    ITEM_TITLE_LINK = "//a[contains(@class, 'font-weight-bold')]"
    # Price column: second col-md-2 in the row (first is item specs area)
    ITEM_PRICE = "//div[contains(@class,'col-md-2')][1]"

    # Total block at the bottom of the cart
    CART_TOTAL = "//h2[contains(text(), 'Итого')]"

    # "Удалить" button inside an item row
    ITEM_REMOVE_BTN = (
        "//a[contains(@class, 'btn-outline-primary') and contains(text(), 'Удалить')]"
    )

    # --- PUBLIC API ---

    def open(self, url_path=""):
        with allure.step("Open cart page"):
            self.open(self.URL)

    @allure.step("Wait for cart to load")
    def wait_for_cart(self):
        self.wait_for_element(self.CART_ITEM)

    @allure.step("Get all product names in cart")
    def get_all_product_names(self) -> list[str]:
        items = self.find(self.CART_ITEM)
        names = []
        for i in range(items.count()):
            name = items.nth(i).locator(self.ITEM_TITLE_LINK).inner_text().strip()
            names.append(name)
        logger.info(f"Cart items: {names}")
        return names

    @allure.step("Get all product hrefs in cart")
    def get_all_product_hrefs(self) -> list[str]:
        items = self.find(self.CART_ITEM)
        hrefs = []
        for i in range(items.count()):
            href = items.nth(i).locator(self.ITEM_TITLE_LINK).get_attribute("href")
            hrefs.append(href)
        logger.info(f"Cart item hrefs: {hrefs}")
        return hrefs

    @allure.step("Check if '{product_href}' is in cart")
    def has_product(self, product_href: str) -> bool:
        hrefs = self.get_all_product_hrefs()
        return any(product_href == href for href in hrefs)

    @allure.step("Get cart total price string")
    def get_total_price(self) -> str:
        """Return raw total string."""
        self.wait_for_element(self.CART_TOTAL)
        return self.get_text(self.CART_TOTAL)

    @allure.step("Get first item price string")
    def get_first_item_price(self) -> str:
        first_item = self.find(f"({self.CART_ITEM})[1]")
        return first_item.locator(self.ITEM_PRICE).inner_text().strip()
