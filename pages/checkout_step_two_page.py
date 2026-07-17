from __future__ import annotations

import os
from playwright.sync_api import Page

APP_URL = os.environ.get("APP_URL", "https://www.saucedemo.com")

ACTION_WAIT_MS = 5_000


class CheckoutStepTwoPage:
    """Page Object for SauceDemo checkout step two (order overview)."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def __repr__(self) -> str:
        return f"CheckoutStepTwoPage(url={self.page.url!r})"

    # ── navigation ────────────────────────────────────────────────────────────

    def navigate(self) -> CheckoutStepTwoPage:
        self.page.goto(f"{APP_URL}/checkout-step-two.html")
        self.page.wait_for_load_state("networkidle")
        self.page.locator(".checkout_summary_container").wait_for(state="visible")
        return self

    # ── actions ───────────────────────────────────────────────────────────────

    def click_finish(self) -> CheckoutCompletePage:
        from pages.checkout_complete_page import CheckoutCompletePage
        self.page.locator("[data-test='finish']").click()
        self.page.wait_for_load_state("networkidle")
        return CheckoutCompletePage(self.page)

    def click_cancel(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage
        self.page.locator("[data-test='cancel']").click()
        self.page.wait_for_load_state("networkidle")
        return InventoryPage(self.page)

    # ── state checks ──────────────────────────────────────────────────────────

    def get_item_names(self) -> list[str]:
        try:
            self.page.locator(".cart_item").first.wait_for(
                state="visible", timeout=ACTION_WAIT_MS
            )
        except Exception:
            return []
        return [
            el.inner_text().strip()
            for el in self.page.locator(".inventory_item_name").all()
        ]

    def get_item_total_text(self) -> str:
        try:
            loc = self.page.locator(".summary_subtotal_label")
            loc.wait_for(state="visible", timeout=ACTION_WAIT_MS)
            return loc.inner_text().strip()
        except Exception:
            return ""

    def get_tax_text(self) -> str:
        try:
            loc = self.page.locator(".summary_tax_label")
            loc.wait_for(state="visible", timeout=ACTION_WAIT_MS)
            return loc.inner_text().strip()
        except Exception:
            return ""

    def get_total_text(self) -> str:
        try:
            loc = self.page.locator(".summary_total_label")
            loc.wait_for(state="visible", timeout=ACTION_WAIT_MS)
            return loc.inner_text().strip()
        except Exception:
            return ""

    def is_on_step_two(self) -> bool:
        try:
            self.page.locator(".checkout_summary_container").wait_for(
                state="visible", timeout=ACTION_WAIT_MS
            )
            return True
        except Exception:
            return False


from pages.checkout_complete_page import CheckoutCompletePage  # noqa: E402
from pages.inventory_page import InventoryPage  # noqa: E402
