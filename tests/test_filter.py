"""
Test 2.1 — Filter products by price range and verify results.
"""

import allure
import pytest
from utils.helpers import parse_price

# Price range to apply.
# The slider snaps to 500-₽ boundaries
# We allow a ±500 tolerance (one slider step) in the assertion.
MIN_PRICE = 25_000
MAX_PRICE = 45_000
TOLERANCE = 500  # one slider step


@allure.feature("Catalog")
@allure.story("Price filter")
@allure.title("Filtering by price range shows only products within that range")
@pytest.mark.parametrize("min_p,max_p", [(MIN_PRICE, MAX_PRICE)])
def test_filter_by_price(catalog, min_p, max_p):
    with allure.step("Open the sofas catalog"):
        catalog.open_catalog()

    with allure.step(f"Apply price filter {min_p}–{max_p} ₽"):
        catalog.filter_by_price_range(min_p, max_p)

    with allure.step("Read the first product's price from the filtered results"):
        info = catalog.get_first_product_info()
        price_str = info["price"]
        price = parse_price(price_str)

    with allure.step(
        f"Assert price {price} ₽ is within [{min_p - TOLERANCE}, {max_p + TOLERANCE}] ₽"
    ):
        assert min_p - TOLERANCE <= price <= max_p + TOLERANCE, (
            f"Expected price in range {min_p - TOLERANCE}–{max_p + TOLERANCE} ₽, "
            f"got {price} ₽ (raw: '{price_str}')"
        )
