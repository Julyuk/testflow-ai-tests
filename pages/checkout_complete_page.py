from __future__ import annotations

import os
from playwright.sync_api import Page

APP_URL = os.environ.get("APP_URL", "https://www.saucedemo.com")
COMPLETE_URL = f"{APP_URL}/checkout-complete.html"

ACTION_WAIT_MS = 5_000


class CheckoutCompletePage:
    """Page Object for SauceDemo checkout complete / order confirmation page."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def __repr__(self) -> str:
        return f"CheckoutCompletePage(url={self.page.url!r})"

    # ── navigation ────────────────────────────────────────────────────────────

    def navigate(self) -> CheckoutCompletePage:
        self.page.goto(COMPLETE_URL)
        self.page.wait_for_load_state("networkidle")
        return self

    # ── actions ───────────────────────────────────────────────────────────────

    def click_back_home(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage
        self.page.locator("[data-test='back-to-products']").click()
        self.page.wait_for_load_state("networkidle")
        return InventoryPage(self.page)

    # ── state checks ──────────────────────────────────────────────────────────

    def is_confirmation_visible(self) -> bool:
        try:
            self.page.locator("[data-test='checkout-complete-container']").wait_for(
                state="visible", timeout=ACTION_WAIT_MS
            )
            return True
        except Exception:
            return False

    def get_confirmation_header(self) -> str:
        try:
            loc = self.page.locator("[data-test='complete-header']")
            loc.wait_for(state="visible", timeout=ACTION_WAIT_MS)
            return loc.inner_text().strip()
        except Exception:
            return ""

    def get_confirmation_text(self) -> str:
        try:
            loc = self.page.locator("[data-test='complete-text']")
            loc.wait_for(state="visible", timeout=ACTION_WAIT_MS)
            return loc.inner_text().strip()
        except Exception:
            return ""

    def is_on_complete_page(self) -> bool:
        return "checkout-complete" in self.page.url


from pages.inventory_page import InventoryPage  # noqa: E402
