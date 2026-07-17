from __future__ import annotations

import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from tests.test_data import (
    VALID_USERNAME,
    VALID_PASSWORD,
    LOCKED_USERNAME,
    LOCKED_PASSWORD,
    INVALID_PASSWORD,
    INVALID_USERNAME,
    ERROR_LOCKED_OUT,
    ERROR_INVALID_CREDENTIALS,
    ERROR_USERNAME_REQUIRED,
    ERROR_PASSWORD_REQUIRED,
    INVENTORY_URL,
    APP_URL,
)


# ── TC-008: Successful login ───────────────────────────────────────────────────

@pytest.mark.smoke
def test_login_when_valid_credentials_expects_inventory_page(page: Page) -> None:
    """TC-008: Successful login with valid credentials redirects to inventory."""
    # Arrange
    print("\u25b6 Step 1: Navigate to login page")
    login_page = LoginPage(page).navigate()
    print("\u2713 Step 1 done: Login page loaded")

    # Act
    print("\u25b6 Step 2: Submit valid credentials")
    inventory_page = login_page.login(VALID_USERNAME, VALID_PASSWORD)
    print("\u2713 Step 2 done: Credentials submitted")

    # Assert
    print("\u25b6 Step 3: Verify redirect to inventory")
    assert inventory_page.is_on_inventory_page(), (
        f"Expected to land on inventory page, but URL is: {page.url!r}"
    )
    assert "inventory" in page.url, (
        f"Expected 'inventory' in URL after login, got: {page.url!r}"
    )
    print("\u2713 Step 3 done: Inventory page confirmed")


# ── TC-009: Navigation shows account indicator after login ────────────────────

@pytest.mark.smoke
def test_login_when_valid_credentials_expects_burger_menu_visible(page: Page) -> None:
    """TC-009: After login the burger menu (account nav) is visible in the header."""
    # Arrange
    print("\u25b6 Step 1: Navigate and log in")
    inventory_page = LoginPage(page).navigate().login(VALID_USERNAME, VALID_PASSWORD)
    print("\u2713 Step 1 done: Logged in")

    # Assert
    print("\u25b6 Step 2: Verify burger menu is present")
    burger = page.get_by_role("button", name="Open Menu", exact=False)
    assert burger.is_visible(), "Burger menu button should be visible after login"
    print("\u2713 Step 2 done: Burger menu visible")


# ── TC-011: Login fails with incorrect password ───────────────────────────────

@pytest.mark.regression
def test_login_when_incorrect_password_expects_error_message(page: Page) -> None:
    """TC-011: Login with wrong password shows an error and stays on login page."""
    # Arrange
    print("\u25b6 Step 1: Navigate to login page")
    login_page = LoginPage(page).navigate()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Submit valid username with wrong password")
    login_page.login_expecting_failure(VALID_USERNAME, INVALID_PASSWORD)
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify error is shown")
    assert login_page.is_error_visible(), "Error message should be visible after bad credentials"
    error_text = login_page.get_error_message()
    assert ERROR_INVALID_CREDENTIALS in error_text, (
        f"Expected error containing '{ERROR_INVALID_CREDENTIALS}', got: '{error_text}'"
    )
    assert login_page.is_on_login_page(), "User should remain on the login page"
    print("\u2713 Step 3 done: Error message confirmed")


# ── TC-012: Login fails with non-existent username ────────────────────────────

@pytest.mark.regression
def test_login_when_nonexistent_user_expects_error_message(page: Page) -> None:
    """TC-012: Login with unregistered username shows an error."""
    # Arrange
    print("\u25b6 Step 1: Navigate to login page")
    login_page = LoginPage(page).navigate()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Submit non-existent username")
    login_page.login_expecting_failure(INVALID_USERNAME, VALID_PASSWORD)
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify error is shown")
    assert login_page.is_error_visible(), "Error message should appear for unknown user"
    error_text = login_page.get_error_message()
    assert error_text, f"Error message text should not be empty, got: '{error_text}'"
    assert login_page.is_on_login_page(), "User should remain on the login page"
    print("\u2713 Step 3 done")


# ── TC-013: Login fails when fields are empty ─────────────────────────────────

@pytest.mark.regression
def test_login_when_empty_fields_expects_username_required_error(page: Page) -> None:
    """TC-013: Submitting empty login form shows a required-field error."""
    # Arrange
    print("\u25b6 Step 1: Navigate to login page")
    login_page = LoginPage(page).navigate()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Click login without filling any field")
    login_page.click_login()
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify validation error")
    assert login_page.is_error_visible(), "Validation error should appear for empty form"
    error_text = login_page.get_error_message()
    assert ERROR_USERNAME_REQUIRED in error_text, (
        f"Expected '{ERROR_USERNAME_REQUIRED}' in error, got: '{error_text}'"
    )
    print("\u2713 Step 3 done")


# ── TC-014: Login with email but empty password ───────────────────────────────

@pytest.mark.regression
def test_login_when_empty_password_expects_password_required_error(page: Page) -> None:
    """TC-014: Submitting login with username but empty password shows password error."""
    # Arrange
    print("\u25b6 Step 1: Navigate to login page")
    login_page = LoginPage(page).navigate()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Fill username only, then click login")
    login_page.fill_username(VALID_USERNAME)
    login_page.click_login()
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify password required error")
    assert login_page.is_error_visible(), "Error should appear when password is empty"
    error_text = login_page.get_error_message()
    assert ERROR_PASSWORD_REQUIRED in error_text, (
        f"Expected '{ERROR_PASSWORD_REQUIRED}' in error, got: '{error_text}'"
    )
    assert login_page.is_on_login_page(), "User should remain on login page"
    print("\u2713 Step 3 done")


# ── TC-069 (auth guard): Protected page redirects unauthenticated user ─────────

@pytest.mark.regression
def test_inventory_when_unauthenticated_direct_navigation_expects_redirect(
    page: Page,
) -> None:
    """TC-069 (auth): Direct navigation to inventory without login redirects to login."""
    # Act
    print("\u25b6 Step 1: Navigate directly to inventory URL without logging in")
    page.goto(INVENTORY_URL)
    page.wait_for_load_state("networkidle")
    print("\u2713 Step 1 done")

    # Assert
    print("\u25b6 Step 2: Verify redirect to login page")
    assert "inventory" not in page.url, (
        f"Unauthenticated user should not access inventory, but URL is: {page.url!r}"
    )
    print("\u2713 Step 2 done: Redirect confirmed")


# ── Locked-out user ────────────────────────────────────────────────────────────

@pytest.mark.regression
def test_login_when_locked_out_user_expects_locked_error(page: Page) -> None:
    """Locked-out user sees a specific error message and cannot log in."""
    # Arrange
    print("\u25b6 Step 1: Navigate to login page")
    login_page = LoginPage(page).navigate()
    print("\u2713 Step 1 done")

    # Act
    print("\u25b6 Step 2: Submit locked-out credentials")
    login_page.login_expecting_failure(LOCKED_USERNAME, LOCKED_PASSWORD)
    print("\u2713 Step 2 done")

    # Assert
    print("\u25b6 Step 3: Verify locked-out error")
    assert login_page.is_error_visible(), "Error should appear for locked-out user"
    error_text = login_page.get_error_message()
    assert ERROR_LOCKED_OUT in error_text, (
        f"Expected locked-out error, got: '{error_text}'"
    )
    print("\u2713 Step 3 done")
