import allure
from pages.base_page import BasePage


class MainPage(BasePage):
    URL = "/"

    # --- LOCATORS ---
    # Search bar
    SEARCH_INPUT = (
        "//header[@id='header-laptop']"
        "//div[contains(@class, 'input-group')]"
        "//input[@name='query']"
    )
    SEARCH_BUTTON = (
        "//header[@id='header-laptop']"
        "//div[contains(@class, 'input-group')]"
        "//button[@type='submit']"
    )

    # Top-level "Каталог" link that reveals the menu on hover
    CATALOG_MENU_TRIGGER = (
        "//header[@id='header-laptop']"
        "//a[contains(@class, 'laptop-header__link_catalog')]"
    )
    # "Мягкая мебель" item in the mega-menu
    MENU_SOFT_FURNITURE = (
        " //div[contains(@class,'menu__bkg')]//a[contains(.,'Мягкая мебель')]"
    )
    # "Диваны" link inside the soft-furniture sub-menu
    SOFAS_LINK = (
        "//div[contains(@class, 'menu-3')]//a[normalize-space(text())='Диваны']"
    )

    # Favorite counter in header
    FAVORITE_COUNTER = (
        "//div[contains(@class, 'header-laptop__favorite')]//a[@href='/favorite/']"
    )

    # Cart link in header
    CART_LINK = "//div[contains(@class, 'header-laptop__cart')]//a[@href='/cart']"

    # --- PUBLIC API ---

    def open_main(self):
        with allure.step("Open main page"):
            super().open(self.URL)

    @allure.step("Search for: {text}")
    def search_for_product(self, text: str):
        self.input_text(self.SEARCH_INPUT, text)
        self.page.keyboard.press("Enter")
        # self.page.wait_for_load_state("networkidle")

    @allure.step("Navigate to 'Диваны' category via menu")
    def go_to_sofas(self):
        # Hover over 'Каталог' to reveal dropdown menu
        self.find(self.CATALOG_MENU_TRIGGER).hover()
        # Wait for 'Мягкая мебель' and hover over it
        self.wait_for_element(self.MENU_SOFT_FURNITURE)
        self.find(self.MENU_SOFT_FURNITURE).hover()
        # Click 'Диваны'
        self.wait_for_element(self.SOFAS_LINK)
        self.click(self.SOFAS_LINK)
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Click cart icon in header")
    def go_to_cart(self):
        self.click(self.CART_LINK)
        self.page.wait_for_load_state("domcontentloaded")

    @allure.step("Click favorites icon in header")
    def go_to_favorites(self):
        self.click(self.FAVORITE_COUNTER)
        self.page.wait_for_load_state("domcontentloaded")
