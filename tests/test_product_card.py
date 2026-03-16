"""
Test 2.2 — Open a product card and verify its name and characteristics.
"""

import allure
from utils.helpers import parse_dimension

# The name of a characteristic that should exist in the product table.
# 'Ширина, мм.' is present for most sofas on this site.
EXPECTED_WIDTH_SPEC = "Ширина, мм."
EXPECTED_DEPTH_SPEC = "Глубина, мм."
DESIRED_PRODUCT = "Диван велюр"


@allure.feature("Product Card")
@allure.story("Product details")
@allure.title("Product page shows correct name and characteristics")
def test_product_card_details(catalog, product):
    with allure.step("Open the sofas catalog"):
        catalog.open_catalog()
        catalog.screenshot("1. Catalog opened")

    with allure.step(f"Find '{DESIRED_PRODUCT}' in catalog and read specs"):
        specs_catalog = catalog.find_product_characteristics_by_name(DESIRED_PRODUCT)
        assert specs_catalog, f"Product '{DESIRED_PRODUCT}' not found on catalog page"
        catalog.screenshot("2. Product found in catalog")
        allure.attach(
            f"Catalog specs: {specs_catalog}",
            name="Catalog product specs",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(f"Click on '{DESIRED_PRODUCT}' to open its page"):
        catalog.click_product_by_name(DESIRED_PRODUCT)

    with allure.step("Wait for product to load"):
        product.wait_for_product_page()
        product.screenshot("3. Product page loaded")

    with allure.step("Read product characteristics from product page"):
        product.open_characteristics_tab()
        product.screenshot("4. Characteristics tab opened")
        width_page = parse_dimension(product.get_characteristic(EXPECTED_WIDTH_SPEC))
        depth_page = parse_dimension(product.get_characteristic(EXPECTED_DEPTH_SPEC))

        allure.attach(
            f"Width: {width_page} mm\nDepth: {depth_page} mm",
            name="Product page specs",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("Verify characteristics match catalog page"):
        assert (
            width_page == specs_catalog["width"]
        ), f"Width mismatch: catalog={specs_catalog['width']} mm, page={width_page} mm"
        assert (
            depth_page == specs_catalog["depth"]
        ), f"Depth mismatch: catalog={specs_catalog['depth']} mm, page={depth_page} mm"
