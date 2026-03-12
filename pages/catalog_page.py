import allure
from pages.base_page import BasePage
from utils.logger import logger
from utils.helpers import parse_dimension

# Step size of the prize slider on site
_PRICE_SLIDER_STEP = 500


class CatalogPage(BasePage):
    URL = "/myagkaya_mebel_v_saratove/divanyi_v_saratove"

    # --- LOCATORS ---
    # FILTER LOCATORS
    # The block that contains the price filter
    PRICE_FILTER_BLOCK = (
        "//div[contains(@class,'filter__item')]"
        "[.//div[contains(@class,'filter__title')]"
        "//a[normalize-space()='Цена']]"
    )
    # Clickable title inside the price filter block (opens slider)
    PRICE_FILTER_TITLE = (
        "//div[contains(@class,'filter__title')]//a[normalize-space()='Цена']"
    )
    PRICE_FILTER_VALUES = (
        f"{PRICE_FILTER_BLOCK}//div[contains(@class,'filter__values')]"
    )
    # Both slider handles live inside the same block
    PRICE_SLIDER_MIN = (
        f"{PRICE_FILTER_VALUES}//div[contains(@class, 'min-slider-handle')]"
    )
    PRICE_SLIDER_MAX = (
        f"{PRICE_FILTER_VALUES}//div[contains(@class, 'max-slider-handle')]"
    )

    PRICE_MIN_VALUE = (
        f"{PRICE_FILTER_VALUES}//div[contains(@class,'range-slider__down')]"
    )
    PRICE_MAX_VALUE = f"{PRICE_FILTER_VALUES}//div[contains(@class,'range-slider__up')]"

    # "Apply filter" link (rendered as <a id="filterLinkContainer">)
    APPLY_FILTER_BTN = (
        "//div[contains(@class, 'filter__list')]//a[@id='filterLinkContainer']"
    )

    # PRODUCT CARD LOCATORS
    # Root of a product card — excludes modifier classes like product-card__name
    PRODUCT_CARD = (
        "//div[contains(@class, 'product-card') "
        "and not(contains(@class, 'product-card__'))]"
    )

    # Specific card by name
    CARD_BY_NAME = (
        "//div[contains(@class, 'product-card__name')]"
        "//a[contains(normalize-space(text()), '{product_name}')]"
    )

    # Find product card ancestor
    CARD_ANCESTOR = (
        "/ancestor::div[contains(@class, 'product-card') "
        "and not(contains(@class, 'product-card__'))]"
    )

    # Relative locators (used with .locator() on a card element)
    CARD_TITLE_LINK = "//div[contains(@class, 'product-card__name')]//a"

    # Current price lives in product-card__now_price > span > b
    # The OLD price is inside a nested div (.product-card__old_price > span),
    # so selecting /span/b from now_price picks only the NEW price.
    CARD_CURRENT_PRICE = "//div[contains(@class, 'product-card__now_price')]/span/b"

    CARD_BUY_BTN = "//a[contains(text(), 'Купить')]"
    CARD_FAV_BTN = "//div[contains(@class, 'product-card__favorites')]//a"

    WIDTH_SPEC = "//small[contains(text(), 'Ширина')]"
    DEPTH_SPEC = "//small[contains(text(), 'Глубина')]"

    # --- PUBLIC API ---
    def open_catalog(self):
        with allure.step("Open sofas catalog"):
            super().open(self.URL)

    @allure.step("Apply price filter: {min_price} - {max_price}")
    def filter_by_price_range(self, min_price: int, max_price: int):
        """
        Open the price filter. Move both sliders to given numbers.
        If value is unreachable, land on the nearest.
        """
        self._open_price_filter()
        self._move_slider_to_value(self.PRICE_SLIDER_MIN, min_price)
        self._move_slider_to_value(self.PRICE_SLIDER_MAX, max_price)
        self._apply_filter()

    @allure.step("Get first product info")
    def get_first_product_info(self) -> dict[str, str]:
        first_card = self.find(f"({self.PRODUCT_CARD})[1]")
        name = first_card.locator(self.CARD_TITLE_LINK).inner_text().strip()
        price = first_card.locator(self.CARD_CURRENT_PRICE).inner_text().strip()
        href = first_card.locator(self.CARD_TITLE_LINK).get_attribute("href")
        logger.info(f"First product: name='{name}', price='{price}', href='{href}'")
        return {"name": name, "price": price, "href": href}

    @allure.step("Click 'Купить' on first product")
    def click_first_product_buy(self):
        self.find(f"({self.PRODUCT_CARD})[1]").locator(self.CARD_BUY_BTN).click()
        # self.page.wait_for_load_state("networkidle")

    @allure.step("Click on product by name: '{product_name}'")
    def click_product_by_name(self, product_name: str):
        """Finds a product on the page and clicks on it."""
        # locator = f"//div[contains(@class, 'product-card__name')]//a[contains(text(), '{product_name}')]"
        locator = self.CARD_BY_NAME.format(product_name=product_name)
        self.wait_for_element(locator)
        self.find(locator).click()
        self.page.wait_for_timeout(1_500)

    @allure.step("Toggle favorite on first product")
    def add_first_product_to_favorites(self):
        self.find(f"({self.PRODUCT_CARD})[1]").locator(self.CARD_FAV_BTN).click()
        self.page.wait_for_timeout(1_500)

    def is_first_product_favorite_active(self) -> bool:
        """
        Return true if the favorite icon of the first card is active.
        """
        classes = (
            self.find(f"({self.PRODUCT_CARD})[1]")
            .locator(self.CARD_FAV_BTN)
            .get_attribute("class")
            or ""
        )
        return "active" in classes

    @allure.step("Find product characteristics")
    def find_product_characteristics_by_name(
        self, product_name: str
    ) -> dict[str, str] | dict[str] | None:
        """
        Returns product_name specifications.
        """
        locator = self.CARD_BY_NAME.format(product_name=product_name)
        product_card = self.find(f"{locator}{self.CARD_ANCESTOR}").first

        if not product_card.is_visible():
            return None

        specs = {}
        width_text = product_card.locator(self.WIDTH_SPEC).inner_text().strip()
        depth_text = product_card.locator(self.DEPTH_SPEC).inner_text().strip()

        specs["width"] = parse_dimension(width_text)
        specs["depth"] = parse_dimension(depth_text)

        return specs

    # --- PRIVATE METHODS ---
    def _open_price_filter(self):
        """Open price filter if it is collapsed."""
        slider_block = self.find(self.PRICE_FILTER_VALUES)

        if not slider_block.is_visible():
            logger.debug("Opening price filter")

            title = self.find(self.PRICE_FILTER_TITLE)
            title.wait_for(state="visible", timeout=5000)
            title.click()

            slider_block.wait_for(state="visible", timeout=5000)

    def _move_slider_to_value(self, handle_xpath: str, target: int):
        """
        Move a slider handle to target by pressing ArrowRight / ArrowLeft keys.
        """
        handle = self.find(handle_xpath)
        handle.wait_for(state="visible", timeout=5_000)
        handle.click()

        current = int(handle.get_attribute("aria-valuenow") or 0)
        if current == target:
            logger.debug(f"Slider already at {target}")
            return

        diff = target - current
        steps = round(abs(diff) / _PRICE_SLIDER_STEP)
        key = "ArrowRight" if diff > 0 else "ArrowLeft"

        logger.info(
            f"Moving slider from {current} to {target} "
            f"({'+' if diff > 0 else ''}{diff} ₽, {steps} steps, {key})"
        )

        for _ in range(steps):
            handle.press(key)

        final = int(handle.get_attribute("aria-valuenow") or 0)
        if final != target:
            logger.warning(
                f"Slider landed on {final} instead of {target}"
                f"(snapped to nearest step boundary)"
            )

    def _apply_filter(self):
        """Click apply-filter and wait for page to reload."""
        apply_btn = self.find(self.APPLY_FILTER_BTN)
        apply_btn.wait_for(state="visible", timeout=5000)
        apply_btn.click()

        # self.page.locator(self.PRODUCT_CARD).first.wait_for()
        self.page.wait_for_load_state("networkidle")
