"""
Test 2.4 — Search for a product by name and verify it appears in results.
"""

import allure

SEARCH_QUERY = "Диван Бостон"


@allure.feature("Search")
@allure.story("Search by product name")
@allure.title("Searching for 'Диван Бостон' returns relevant results")
def test_search_product(main, search_results):
    with allure.step("Open the main page"):
        main.open_main()

    with allure.step(f"Enter search query '{SEARCH_QUERY}' and submit"):
        main.search_for_product(SEARCH_QUERY)

    with allure.step("Wait for search results to appear"):
        search_results.wait_for_results()

    with allure.step("Get the name of the first search result"):
        first_name = search_results.get_first_product_name()
        allure.attach(
            first_name,
            name="First search result",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(f"Verify the first result contains '{SEARCH_QUERY}'"):
        assert SEARCH_QUERY.lower() in first_name.lower(), (
            f"Expected first result to contain '{SEARCH_QUERY}', got '{first_name}'"
        )
