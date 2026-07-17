from __future__ import annotations

import os
from playwright.sync_api import Page

APP_URL = os.environ.get("APP_URL", "https://www.saucedemo.com")

ACTION_WAIT_MS = 5_000


class LoginPage:
    """Page Object for the SauceDemo login page."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def __repr__(self) -> str:
        return f"LoginPage(url={self.page.url!r})"

    # ── navigation ────────────────────────────────────────────────────────────

    def navigate(self) -> LoginPage:
        """Go to the login page and wait until the form is ready."""
        self.page.goto(APP_URL)
        self.page.wait_for_load_state("networkidle")
        self.page.locator("[data-test='username']").wait_for(state="visible")
        return self

    # ── actions ───────────────────────────────────────────────────────────────

    def fill_username(self, username: str) -> LoginPage:
        self.page.locator("[data-test='username']").fill(username)
        return self

    def fill_password(self, password: str) -> LoginPage:
        self.page.locator("[data-test='password']").fill(password)
        return self

    def click_login(self) -> None:
        self.page.locator("[data-test='login-button']").click()

    def login(self, username: str, password: str) -> InventoryPage:
        """Fill credentials and submit; return the resulting InventoryPage."""
        from pages.inventory_page import InventoryPage
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()
        self.page.wait_for_load_state("networkidle")
        return InventoryPage(self.page)

    def login_expecting_failure(self, username: str, password: str) -> LoginPage:
        """Submit credentials that are expected to fail; stay on login page."""
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()
        return self

    # ── state checks ──────────────────────────────────────────────────────────

    def is_error_visible(self) -> bool:
        try:
            self.page.locator("[data-test='error']").wait_for(
                state="visible", timeout=ACTION_WAIT_MS
            )
            return True
        except Exception:
            return False

    def get_error_message(self) -> str:
        try:
            self.page.locator("[data-test='error']").wait_for(
                state="visible", timeout=ACTION_WAIT_MS
            )
            return self.page.locator("[data-test='error']").inner_text().strip()
        except Exception:
            return ""

    def is_on_login_page(self) -> bool:
        try:
            self.page.locator("[data-test='login-button']").wait_for(
                state="visible", timeout=ACTION_WAIT_MS
            )
            return True
        except Exception:
            return False
