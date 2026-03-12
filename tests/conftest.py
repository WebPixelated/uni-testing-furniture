"""
Test-level fixtures.
Each fixture returns a ready-to-use Page Object bound to the current `page`.
"""

import pytest
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.favorite_page import FavoritePage
from pages.main_page import MainPage
from pages.search_results_page import SearchResultsPage


@pytest.fixture
def catalog(page):
    return CatalogPage(page)


@pytest.fixture
def product(page):
    return ProductPage(page)


@pytest.fixture
def cart(page):
    return CartPage(page)


@pytest.fixture
def favorites(page):
    return FavoritePage(page)


@pytest.fixture
def main(page):
    return MainPage(page)


@pytest.fixture
def search_results(page):
    return SearchResultsPage(page)
