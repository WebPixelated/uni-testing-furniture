"""
Test 2.3 — Add the first product to favourites and verify it appears on the
           favourites page with the heart icon in the active (green) state.
"""

import allure


@allure.feature("Favourites")
@allure.story("Add to favourites")
@allure.title("Adding a product to favourites updates icon state and favourites page")
def test_add_to_favorites(catalog, favorites):
    with allure.step("Open the sofas catalog"):
        catalog.open_catalog()

    with allure.step("Get first product href"):
        info = catalog.get_first_product_info()
        product_href = info["href"]
        allure.attach(
            product_href,
            name="Product added to favourites",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Click the heart icon on the first product"):
        catalog.add_first_product_to_favorites()

    with allure.step("Verify the heart icon is now active (green)"):
        assert catalog.is_first_product_favorite_active(), (
            "Favourite icon does not have the 'active' class after being clicked"
        )

    with allure.step("Navigate to the favourites page"):
        catalog.page.goto(f"{catalog.BASE_URL}/favorite/")
        catalog.page.wait_for_load_state("domcontentloaded")

    with allure.step("Wait for favourite items to load (AJAX)"):
        favorites.wait_for_products_to_load()

    with allure.step("Verify product appears in the favourites list"):
        assert favorites.is_product_in_favorites_by_href(product_href), (
            f"Product '{product_href}' was not found on the favourites page. "
            f"Found: {favorites.get_all_product_names()}"
        )
