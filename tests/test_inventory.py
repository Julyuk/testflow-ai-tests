from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.test_data import (
    VALID_USERNAME,
    VALID_PASSWORD,
    EXPECTED_PRODUCT_COUNT,
    PRODUCT_BACKPACK,
    PRODUCT_BIKE_LIGHT,
    ALL_PRODUCTS,
    MAX_LOOP_ITERATIONS,
)


# ── TC-036: Cart badge increments when product is added ───────────────────────

@pytest.mark.smoke
def test_cart_badge_when_product_added_expects_count_increments(page: Page) -> None:
    """TC-036: Cart item count increases by 1 after adding a product."""
    # Arrange
    print("\u25b6 Step 1: Log in and navigate to inventory")
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    initial_count = inventory_page.get_cart_badge_count()
    print(f"\u2713 Step 1 done: Initial cart count = {initial_count}")

    # Act
    print("\u25b6 Step 2: Add one product to cart")
    inventory_page.click_add_to_cart_for_item(PRODUCT_BACKPACK)
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify badge incremented")
    new_count = inventory_page.get_cart_badge_count()
    assert new_count == initial_count + 1, (
        f"Expected cart count {initial_count + 1}, got {new_count}"
    )
    print(f"\u2713 Step 3 done: Cart count is now {new_count}")


# ── TC-035: Product appears in cart after Add to Cart ─────────────────────────

@pytest.mark.smoke
def test_add_to_cart_when_product_added_expects_item_in_cart(page: Page) -> None:
    """TC-035: Product is listed in the shopping cart after clicking Add to Cart."""
    # Arrange
    print("\u25b6 Step 1: Log in")
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Add product to cart")
    inventory_page.click_add_to_cart_for_item(PRODUCT_BACKPACK)
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Navigate to cart and verify item present")
    cart_page = inventory_page.click_cart_icon()
    assert cart_page.is_item_in_cart(PRODUCT_BACKPACK), (
        f"Expected '{PRODUCT_BACKPACK}' to be in cart, but it was not found"
    )
    print("\u2713 Step 3 done: Item confirmed in cart")


# ── TC-039: Remove button appears after adding; item removed from cart ─────────

@pytest.mark.smoke
def test_remove_button_when_item_added_expects_button_visible(page: Page) -> None:
    """TC-039 (inventory side): Remove button is visible after adding a product."""
    # Arrange
    print("\u25b6 Step 1: Log in")
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Add product")
    inventory_page.click_add_to_cart_for_item(PRODUCT_BACKPACK)
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify Remove button is visible")
    assert inventory_page.is_remove_button_visible_for_item(PRODUCT_BACKPACK), (
        f"Remove button should be visible for '{PRODUCT_BACKPACK}' after adding to cart"
    )
    print("\u2713 Step 3 done")


# ── TC-040: Cart badge decrements after removal ───────────────────────────────

@pytest.mark.regression
def test_cart_badge_when_item_removed_expects_count_decrements(page: Page) -> None:
    """TC-040: Cart item count decreases by 1 after removing a product."""
    # Arrange
    print("\u25b6 Step 1: Log in and add two products")
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    inventory_page.click_add_to_cart_for_item(PRODUCT_BACKPACK)
    inventory_page.click_add_to_cart_for_item(PRODUCT_BIKE_LIGHT)
    count_after_add = inventory_page.get_cart_badge_count()
    print(f"\u2713 Step 1 done: Cart count after adding = {count_after_add}")

    # Act
    print("\u25b6 Step 2: Remove one product")
    inventory_page.click_remove_for_item(PRODUCT_BACKPACK)
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify badge decremented")
    count_after_remove = inventory_page.get_cart_badge_count()
    assert count_after_remove == count_after_add - 1, (
        f"Expected cart count {count_after_add - 1}, got {count_after_remove}"
    )
    print(f"\u2713 Step 3 done: Cart count is now {count_after_remove}")


# ── Inventory product count ────────────────────────────────────────────────────

@pytest.mark.smoke
def test_inventory_when_logged_in_expects_correct_product_count(page: Page) -> None:
    """Inventory page displays the expected number of products."""
    # Arrange
    print("\u25b6 Step 1: Log in")
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    print("\u2713 Step 1 done")

    # Assert
    print("\u25b6 Step 2: Count products")
    count = inventory_page.get_inventory_item_count()
    assert count == EXPECTED_PRODUCT_COUNT, (
        f"Expected {EXPECTED_PRODUCT_COUNT} products, got {count}"
    )
    print(f"\u2713 Step 2 done: Found {count} products")


# ── Sort: price low to high ────────────────────────────────────────────────────

@pytest.mark.regression
def test_sort_when_price_low_to_high_expects_ascending_prices(page: Page) -> None:
    """Sorting by price low-to-high returns prices in ascending order."""
    # Arrange
    print("\u25b6 Step 1: Log in")
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Select sort option lohi")
    inventory_page.select_sort_option("lohi")
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify prices are ascending")
    prices = inventory_page.get_item_prices()
    assert len(prices) > 0, "Expected at least one price to be returned"
    assert prices == sorted(prices), (
        f"Prices should be ascending after lohi sort, got: {prices}"
    )
    print(f"\u2713 Step 3 done: Prices in order: {prices}")
