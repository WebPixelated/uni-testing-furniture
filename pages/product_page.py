import allure
from pages.base_page import BasePage
from utils.logger import logger


class ProductPage(BasePage):
    # --- LOCATORS ---
    PRODUCT_H1 = "//h1[@itemprop='name']"

    # Current price on the product page
    PRODUCT_PRICE = "//span[@itemprop='price' and contains(@class, 'productPrice')]"

    # Favourite icon on the product page
    FAV_ICON = "//div[contains(@class, 'page-product__favorite')]//a[contains(@class, 'favorite-icon')]"

    # Action buttons
    ADD_TO_CART_BTN = "//a[contains(text(), 'В корзину')]"
    BUY_ONE_CLICK_BTN = "//button[contains(text(), 'Купить 1 клик')]"

    # Characteristics table (tab "Характеристики")
    CHAR_BUTTON = "//a[@id='singleProdParamTab']"
    CHAR_TABLE = "//div[@id='singleProdParam']//table//tbody"
    # Row by characteristic name: e.g. _char_row("Ширина, мм.")
    _CHAR_ROW = "//div[@id='singleProdParam']//table//tr[td[1][normalize-space(text())='{name}']]"

    # --- PUBLIC API ---

    @allure.step("Wait for product page to load")
    def wait_for_product_page(self):
        self.wait_for_element(self.PRODUCT_H1)

    @allure.step("Get product name (H1)")
    def get_product_name(self) -> str:
        self.wait_for_element(self.PRODUCT_H1)
        return self.get_text(self.PRODUCT_H1)

    @allure.step("Get product price from product page")
    def get_price(self) -> str:
        """Return the raw price string."""
        self.wait_for_element(self.PRODUCT_PRICE)
        return self.get_text(self.PRODUCT_PRICE)

    @allure.step("Open characteristics tab")
    def open_characteristics_tab(self):
        """
        Click the characteristics tab button.
        Waits for table if it appears. Table may not exist.
        """
        self.wait_for_element(self.CHAR_BUTTON)
        self.click(self.CHAR_BUTTON)
        try:
            self.wait_for_element(self.CHAR_TABLE, timeout=2_000)
        except Exception:
            logger.info("Characteristics table did not appear for this product.")

    @allure.step("Get characteristics value for '{name}'")
    def get_characteristic(self, name: str) -> str | None:
        row_xpath = self._CHAR_ROW.format(name=name)
        try:
            self.wait_for_element(row_xpath, timeout=5_000)
            # Second <td> holds the value
            value = self.find(f"{row_xpath}/td[2]").inner_text().strip()
            logger.info(f"Characteristic '{name}' = '{value}'")
            return value
        except Exception:
            logger.warning(f"Characteristic '{name}' not found on page")
            return None

    @allure.step("Click 'В корзину' (handle confirmation alert)")
    def add_to_cart(self, accept_redirect: bool = True):
        """
        Dialogue is shown when adding goods to cart from product page.
        Accept the dialogue to proceed to cart page, or dismiss it.
        """

        self.page.wait_for_load_state("networkidle")

        self.wait_for_element(self.ADD_TO_CART_BTN)

        def _handle_dialog(dialog):
            logger.info(
                f"Dialog appeared: '{dialog.message}' - "
                f"{'accepting' if accept_redirect else 'dismissing'}"
            )
            if accept_redirect:
                dialog.accept()
            else:
                dialog.dismiss()

        self.page.once("dialog", _handle_dialog)
        self.click(self.ADD_TO_CART_BTN)

        if accept_redirect:
            try:
                self.page.wait_for_url("**/cart*", timeout=5000)
                logger.info("Successfully redirected to cart page.")
            except Exception:
                logger.warning(
                    "URL did not change to /cart in time. Perhaps the site uses AJAX for cart?"
                )
