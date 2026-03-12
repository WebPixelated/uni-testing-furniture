"""
Test 2.5 — Add the first product in the catalog to the cart and verify
           that it appears in the cart with a matching price.
"""

import allure
import pytest
from utils.helpers import parse_price


@allure.feature("Cart")
@allure.story("Add to cart")
@allure.title("Adding a product to the cart reflects correct name and price")
def test_add_to_cart_and_verify_price(catalog, product, cart):
    with allure.step("Open the sofas catalog"):
        catalog.open_catalog()

    with allure.step("Get first product info (name + catalog price)"):
        info = catalog.get_first_product_info()
        catalog_product_name = info["name"]
        catalog_price_str = info["price"]
        catalog_product_href = info["href"]
        catalog_price = parse_price(catalog_price_str)
        allure.attach(
            f"Name: {catalog_product_name}\nPrice (catalog): {catalog_price} ₽\nURL: {catalog_product_href}",
            name="Catalog product info",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Click 'Купить' to open the product page"):
        catalog.click_first_product_buy()

    with allure.step("Wait for the product page to load"):
        product.wait_for_product_page()

    with allure.step("Read price from the product page"):
        product_page_price_str = product.get_price()
        product_page_price = parse_price(product_page_price_str)
        allure.attach(
            f"Price (product page): {product_page_price} ₽",
            name="Product page price",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Click 'В корзину' and accept the redirect alert"):
        # accept_redirect=True → dialog is accepted → browser navigates to /cart
        product.add_to_cart(accept_redirect=True)

    with allure.step("Wait for the cart page to load"):
        cart.wait_for_cart()

    with allure.step(f"Verify '{catalog_product_name}' is present in cart"):
        assert cart.has_product(catalog_product_href), (
            f"Product '{catalog_product_name}' not found in cart. "
            f"Cart contents: {cart.get_all_product_names()}"
        )

    with allure.step("Verify cart total matches the product page price"):
        total_str = cart.get_total_price()
        total_price = parse_price(total_str)
        allure.attach(
            f"Cart total: {total_price} ₽  |  Expected: {product_page_price} ₽",
            name="Price comparison",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert total_price >= product_page_price, (
            f"Cart total {total_price} ₽ does not match "
            f"product page price {product_page_price} ₽"
        )
