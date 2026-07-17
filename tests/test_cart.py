from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.cart_page import CartPage
from tests.test_data import (
    VALID_USERNAME,
    VALID_PASSWORD,
    PRODUCT_BACKPACK,
    PRODUCT_BIKE_LIGHT,
    CART_URL,
)


# ── TC-039: Product removed from cart ─────────────────────────────────────────

@pytest.mark.smoke
def test_remove_from_cart_when_item_removed_expects_item_gone(page: Page) -> None:
    """TC-039: Clicking Remove on a cart item removes it from the cart."""
    # Arrange
    print("\u25b6 Step 1: Log in and add two products")
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    inventory_page.click_add_to_cart_for_item(PRODUCT_BACKPACK)
    inventory_page.click_add_to_cart_for_item(PRODUCT_BIKE_LIGHT)
    cart_page = inventory_page.click_cart_icon()
    print("\u2713 Step 1 done: Cart has two items")

    # Act
    print("\u25b6 Step 2: Remove one item")
    cart_page.click_remove_for_item(PRODUCT_BACKPACK)
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify item is gone, other item remains")
    assert not cart_page.is_item_in_cart(PRODUCT_BACKPACK), (
        f"'{PRODUCT_BACKPACK}' should have been removed from cart"
    )
    assert cart_page.is_item_in_cart(PRODUCT_BIKE_LIGHT), (
        f"'{PRODUCT_BIKE_LIGHT}' should still be in cart"
    )
    print("\u2713 Step 3 done")


# ── TC-041: Empty state when last item removed ────────────────────────────────

@pytest.mark.regression
def test_cart_when_last_item_removed_expects_empty_cart(page: Page) -> None:
    """TC-041: Removing the last item leaves the cart empty."""
    # Arrange
    print("\u25b6 Step 1: Log in and add one product")
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    inventory_page.click_add_to_cart_for_item(PRODUCT_BACKPACK)
    cart_page = inventory_page.click_cart_icon()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Remove the only item")
    cart_page.click_remove_for_item(PRODUCT_BACKPACK)
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify cart is empty")
    assert cart_page.is_cart_empty(), "Cart should be empty after removing the last item"
    badge_count = cart_page.get_cart_badge_count()
    assert badge_count == 0, (
        f"Cart badge should show 0 after removing last item, got {badge_count}"
    )
    print("\u2713 Step 3 done")


# ── TC-040: Cart badge decrements after removal ───────────────────────────────

@pytest.mark.regression
def test_cart_badge_when_item_removed_from_cart_page_expects_decrement(
    page: Page,
) -> None:
    """TC-040: Cart badge count decreases by 1 after removing an item on cart page."""
    # Arrange
    print("\u25b6 Step 1: Log in and add two products")
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    inventory_page.click_add_to_cart_for_item(PRODUCT_BACKPACK)
    inventory_page.click_add_to_cart_for_item(PRODUCT_BIKE_LIGHT)
    cart_page = inventory_page.click_cart_icon()
    count_before = cart_page.get_cart_item_count()
    print(f"\u2713 Step 1 done: Items in cart = {count_before}")

    # Act
    print("\u25b6 Step 2: Remove one item")
    cart_page.click_remove_for_item(PRODUCT_BACKPACK)
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify item count decreased")
    count_after = cart_page.get_cart_item_count()
    assert count_after == count_before - 1, (
        f"Expected {count_before - 1} items after removal, got {count_after}"
    )
    print(f"\u2713 Step 3 done: Item count is now {count_after}")


# ── Cart page accessible after login ──────────────────────────────────────────

@pytest.mark.smoke
def test_cart_when_navigated_directly_expects_page_loads(page: Page) -> None:
    """Cart page loads correctly when navigated to directly after login."""
    # Arrange
    print("\u25b6 Step 1: Log in")
    LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Navigate directly to cart URL")
    cart_page = CartPage(page).navigate()
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify cart page loaded")
    assert "cart" in page.url, (
        f"Expected cart URL, got: {page.url!r}"
    )
    print("\u2713 Step 3 done")


# ── TC-069 (cart): Unauthenticated access to cart redirects ───────────────────

@pytest.mark.regression
def test_cart_when_unauthenticated_direct_navigation_expects_redirect(
    page: Page,
) -> None:
    """TC-069 (cart): Direct navigation to cart without login redirects to login."""
    # Act
    print("\u25b6 Step 1: Navigate directly to cart URL without logging in")
    page.goto(CART_URL)
    page.wait_for_load_state("networkidle")
    print("\u2713 Step 1 done")

    # Assert
    print("\u25b6 Step 2: Verify redirect")
    assert "cart" not in page.url, (
        f"Unauthenticated user should not access cart, but URL is: {page.url!r}"
    )
    print("\u2713 Step 2 done")
