"""
Test 2.3 — Add the first product to favorites and verify it appears on the
           favorites page with the heart icon in the active (green) state.
"""

import allure


@allure.feature("Favorites")
@allure.story("Add to favorites")
@allure.title("Adding a product to favorites updates icon state and favorites page")
def test_add_to_favorites(catalog, favorites):
    with allure.step("Open the sofas catalog"):
        catalog.open_catalog()
        catalog.screenshot("1. Catalog before adding to favorites")

    with allure.step("Get first product href"):
        info = catalog.get_first_product_info()
        product_href = info["href"]
        allure.attach(
            product_href,
            name="Product added to favorites",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Click the heart icon on the first product"):
        catalog.add_first_product_to_favorites()
        catalog.screenshot("2. After clicking favorite icon (should be green)")

    with allure.step("Verify the heart icon is now active (green)"):
        assert (
            catalog.is_first_product_favorite_active()
        ), "Favorite icon does not have the 'active' class after being clicked"

    with allure.step("Navigate to the favorites page"):
        catalog.page.goto(f"{catalog.BASE_URL}/favorite/")
        catalog.page.wait_for_load_state("domcontentloaded")

    with allure.step("Wait for favorite items to load"):
        favorites.wait_for_products_to_load()
        favorites.screenshot("3. Favorites page - product present")

    with allure.step("Verify product appears in the favorites list"):
        assert favorites.is_product_in_favorites_by_href(product_href), (
            f"Product '{product_href}' was not found on the favorites page. "
            f"Found: {favorites.get_all_product_names()}"
        )

    # with allure.step("[CLEANUP] Remove product from favorites to restore state"):
    #     _remove_all_from_favorites(favorites)
    #     favorites.screenshot("4. Favorites page after cleanup")


# def _remove_all_from_favorites(favorites):
#     """
#     Click all 'remove' buttons and reload until the favorites list is empty.
#     Each removal triggers a page reload (site behavior), so we re-query after each.
#     """
#     while True:
#         remove_btns = favorites.find(favorites.CARD_REMOVE_BTN)
#         if remove_btns.count() == 0:
#             break

#         remove_btns.first.click()
#         favorites.page.wait_for_load_state("domcontentloaded")
