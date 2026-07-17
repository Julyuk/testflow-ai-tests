from __future__ import annotations

import os
from playwright.sync_api import Page

APP_URL = os.environ.get("APP_URL", "https://www.saucedemo.com")
CART_URL = f"{APP_URL}/cart.html"

ACTION_WAIT_MS = 5_000


class CartPage:
    """Page Object for the SauceDemo shopping cart page."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def __repr__(self) -> str:
        return f"CartPage(url={self.page.url!r})"

    # ── navigation ────────────────────────────────────────────────────────────

    def navigate(self) -> CartPage:
        self.page.goto(CART_URL)
        self.page.wait_for_load_state("networkidle")
        self.page.locator(".cart_contents_container").wait_for(state="visible")
        return self

    # ── actions ───────────────────────────────────────────────────────────────

    def click_remove_for_item(self, item_name: str) -> CartPage:
        item = self.page.locator(".cart_item").filter(
            has=self.page.get_by_text(item_name, exact=False)
        )
        btn = item.get_by_role("button", name="Remove", exact=False)
        btn.wait_for(state="visible", timeout=ACTION_WAIT_MS)
        btn.click()
        return self

    def click_continue_shopping(self) -> InventoryPage:
        from pages.inventory_page import InventoryPage
        self.page.locator("[data-test='continue-shopping']").click()
        self.page.wait_for_load_state("networkidle")
        return InventoryPage(self.page)

    def click_checkout(self) -> CheckoutStepOnePage:
        from pages.checkout_step_one_page import CheckoutStepOnePage
        self.page.locator("[data-test='checkout']").click()
        self.page.wait_for_load_state("networkidle")
        return CheckoutStepOnePage(self.page)

    # ── state checks ──────────────────────────────────────────────────────────

    def get_cart_item_names(self) -> list[str]:
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

    def get_cart_item_count(self) -> int:
        try:
            self.page.locator(".cart_item").first.wait_for(
                state="visible", timeout=ACTION_WAIT_MS
            )
        except Exception:
            return 0
        return len(self.page.locator(".cart_item").all())

    def is_item_in_cart(self, item_name: str) -> bool:
        return item_name in self.get_cart_item_names()

    def is_cart_empty(self) -> bool:
        try:
            self.page.locator(".cart_item").first.wait_for(
                state="visible", timeout=2_000
            )
            return False
        except Exception:
            return True

    def get_cart_badge_count(self) -> int:
        badge = self.page.locator("[data-test='shopping-cart-badge']")
        try:
            badge.wait_for(state="visible", timeout=ACTION_WAIT_MS)
        except Exception:
            return 0
        text = badge.inner_text().strip()
        return int(text) if text.isdigit() else 0


from pages.checkout_step_one_page import CheckoutStepOnePage  # noqa: E402
from pages.inventory_page import InventoryPage  # noqa: E402
