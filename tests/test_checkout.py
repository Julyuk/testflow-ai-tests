from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.checkout_step_one_page import CheckoutStepOnePage
from pages.checkout_complete_page import CheckoutCompletePage
from tests.test_data import (
    VALID_USERNAME,
    VALID_PASSWORD,
    PRODUCT_BACKPACK,
    PRODUCT_BIKE_LIGHT,
    CHECKOUT_FIRST_NAME,
    CHECKOUT_LAST_NAME,
    CHECKOUT_POSTAL_CODE,
    ERROR_FIRST_NAME_REQUIRED,
    ERROR_LAST_NAME_REQUIRED,
    ERROR_POSTAL_CODE_REQUIRED,
    ORDER_COMPLETE_HEADER,
    CHECKOUT_COMPLETE_URL,
    CHECKOUT_ONE_URL,
)


def _login_and_add_products(page: Page, *product_names: str) -> None:
    """Helper: log in and add the given products to the cart."""
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    for name in product_names:
        inventory_page.click_add_to_cart_for_item(name)


# ── TC-050: Valid delivery info proceeds to step two ──────────────────────────

@pytest.mark.smoke
def test_checkout_step_one_when_valid_info_expects_proceed_to_step_two(
    page: Page,
) -> None:
    """TC-050: Valid delivery address proceeds to checkout step two."""
    # Arrange
    print("\u25b6 Step 1: Log in, add product, navigate to checkout")
    _login_and_add_products(page, PRODUCT_BACKPACK)
    inventory_page_obj = page  # page is already on inventory
    from pages.inventory_page import InventoryPage
    inv = InventoryPage(page)
    cart_page = inv.click_cart_icon()
    step_one = cart_page.click_checkout()
    print("\u2713 Step 1 done: On checkout step one")

    # Act
    print("\u25b6 Step 2: Fill valid delivery info and continue")
    step_two = (
        step_one
        .fill_delivery_info(CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME, CHECKOUT_POSTAL_CODE)
        .click_continue()
    )
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify we are on step two")
    assert step_two.is_on_step_two(), (
        f"Expected to be on checkout step two, but URL is: {page.url!r}"
    )
    print("\u2713 Step 3 done")


# ── TC-051: Empty delivery form shows validation errors ───────────────────────

@pytest.mark.regression
def test_checkout_step_one_when_empty_fields_expects_validation_errors(
    page: Page,
) -> None:
    """TC-051: Submitting empty delivery form shows required-field errors."""
    # Arrange
    print("\u25b6 Step 1: Log in, add product, navigate to checkout step one")
    _login_and_add_products(page, PRODUCT_BACKPACK)
    from pages.inventory_page import InventoryPage
    cart_page = InventoryPage(page).click_cart_icon()
    step_one = cart_page.click_checkout()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Click continue without filling any field")
    step_one.click_continue_expecting_error()
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify error is shown")
    assert step_one.is_error_visible(), "Validation error should appear for empty form"
    error_text = step_one.get_error_message()
    assert error_text, f"Error message should not be empty, got: '{error_text}'"
    assert step_one.is_on_step_one(), "User should remain on checkout step one"
    print(f"\u2713 Step 3 done: Error = '{error_text}'")


# ── TC-051 variant: missing first name ────────────────────────────────────────

@pytest.mark.regression
def test_checkout_step_one_when_missing_first_name_expects_first_name_error(
    page: Page,
) -> None:
    """TC-051 (variant): Missing first name shows first-name required error."""
    # Arrange
    print("\u25b6 Step 1: Log in, add product, navigate to checkout step one")
    _login_and_add_products(page, PRODUCT_BACKPACK)
    from pages.inventory_page import InventoryPage
    cart_page = InventoryPage(page).click_cart_icon()
    step_one = cart_page.click_checkout()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Fill last name and postal code only")
    step_one.fill_last_name(CHECKOUT_LAST_NAME)
    step_one.fill_postal_code(CHECKOUT_POSTAL_CODE)
    step_one.click_continue_expecting_error()
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify first name error")
    assert step_one.is_error_visible(), "Error should appear when first name is missing"
    error_text = step_one.get_error_message()
    assert ERROR_FIRST_NAME_REQUIRED in error_text, (
        f"Expected '{ERROR_FIRST_NAME_REQUIRED}' in error, got: '{error_text}'"
    )
    print("\u2713 Step 3 done")


# ── TC-058: Order confirmation page shown after checkout ──────────────────────

@pytest.mark.smoke
def test_checkout_when_completed_expects_confirmation_page(page: Page) -> None:
    """TC-058: Completing all checkout steps shows the order confirmation page."""
    # Arrange
    print("\u25b6 Step 1: Log in and add a product")
    _login_and_add_products(page, PRODUCT_BACKPACK)
    from pages.inventory_page import InventoryPage
    cart_page = InventoryPage(page).click_cart_icon()
    step_one = cart_page.click_checkout()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Complete checkout")
    step_two = step_one.fill_delivery_info(
        CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME, CHECKOUT_POSTAL_CODE
    ).click_continue()
    complete_page = step_two.click_finish()
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify confirmation page")
    assert complete_page.is_confirmation_visible(), (
        "Order confirmation container should be visible after checkout"
    )
    header = complete_page.get_confirmation_header()
    assert ORDER_COMPLETE_HEADER in header, (
        f"Expected confirmation header '{ORDER_COMPLETE_HEADER}', got: '{header}'"
    )
    assert complete_page.is_on_complete_page(), (
        f"Expected checkout-complete URL, got: {page.url!r}"
    )
    print(f"\u2713 Step 3 done: Confirmation header = '{header}'")


# ── TC-060: Confirmation page shows order summary ─────────────────────────────

@pytest.mark.regression
def test_checkout_step_two_when_items_added_expects_items_in_summary(
    page: Page,
) -> None:
    """TC-060: Checkout step two (overview) lists the items added to cart."""
    # Arrange
    print("\u25b6 Step 1: Log in and add two products")
    _login_and_add_products(page, PRODUCT_BACKPACK, PRODUCT_BIKE_LIGHT)
    from pages.inventory_page import InventoryPage
    cart_page = InventoryPage(page).click_cart_icon()
    step_one = cart_page.click_checkout()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Proceed to step two")
    step_two = step_one.fill_delivery_info(
        CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME, CHECKOUT_POSTAL_CODE
    ).click_continue()
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify items in summary")
    item_names = step_two.get_item_names()
    assert len(item_names) > 0, "Order summary should list at least one item"
    assert PRODUCT_BACKPACK in item_names, (
        f"Expected '{PRODUCT_BACKPACK}' in summary, got: {item_names}"
    )
    assert PRODUCT_BIKE_LIGHT in item_names, (
        f"Expected '{PRODUCT_BIKE_LIGHT}' in summary, got: {item_names}"
    )
    total_text = step_two.get_total_text()
    assert total_text, "Total price should be displayed on the order summary"
    print(f"\u2713 Step 3 done: Items = {item_names}, Total = '{total_text}'")


# ── TC-061: Confirmation page not accessible without placing order ─────────────

@pytest.mark.regression
def test_checkout_complete_when_accessed_directly_without_order_expects_redirect(
    page: Page,
) -> None:
    """TC-061: Direct navigation to checkout-complete without an order redirects away."""
    # Act
    print("\u25b6 Step 1: Navigate directly to checkout-complete URL without login")
    page.goto(CHECKOUT_COMPLETE_URL)
    page.wait_for_load_state("networkidle")
    print("\u2713 Step 1 done")

    # Assert
    print("\u25b6 Step 2: Verify redirect")
    assert "checkout-complete" not in page.url, (
        f"Should not access checkout-complete without a valid order, URL: {page.url!r}"
    )
    print("\u2713 Step 2 done")


# ── TC-051 variant: missing postal code ───────────────────────────────────────

@pytest.mark.regression
def test_checkout_step_one_when_missing_postal_code_expects_postal_error(
    page: Page,
) -> None:
    """TC-052 (postal): Missing postal code shows postal code required error."""
    # Arrange
    print("\u25b6 Step 1: Log in, add product, navigate to checkout step one")
    _login_and_add_products(page, PRODUCT_BACKPACK)
    from pages.inventory_page import InventoryPage
    cart_page = InventoryPage(page).click_cart_icon()
    step_one = cart_page.click_checkout()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Fill name fields but leave postal code empty")
    step_one.fill_first_name(CHECKOUT_FIRST_NAME)
    step_one.fill_last_name(CHECKOUT_LAST_NAME)
    step_one.click_continue_expecting_error()
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify postal code error")
    assert step_one.is_error_visible(), "Error should appear when postal code is missing"
    error_text = step_one.get_error_message()
    assert ERROR_POSTAL_CODE_REQUIRED in error_text, (
        f"Expected '{ERROR_POSTAL_CODE_REQUIRED}' in error, got: '{error_text}'"
    )
    print("\u2713 Step 3 done")
