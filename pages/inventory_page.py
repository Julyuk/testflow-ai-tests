from __future__ import annotations

import os
from playwright.sync_api import Page

APP_URL = os.environ.get("APP_URL", "https://www.saucedemo.com")
INVENTORY_URL = f"{APP_URL}/inventory.html"

ACTION_WAIT_MS = 5_000
MAX_ITERATIONS = 50


class InventoryPage:
    """Page Object for the SauceDemo inventory / product listing page."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def __repr__(self) -> str:
        return f"InventoryPage(url={self.page.url!r})"

    # ── navigation ────────────────────────────────────────────────────────────

    def navigate(self) -> InventoryPage:
        self.page.goto(INVENTORY_URL)
        self.page.wait_for_load_state("networkidle")
        self.page.locator(".inventory_list").wait_for(state="visible")
        return self

    # ── actions ───────────────────────────────────────────────────────────────

    def open_burger_menu(self) -> InventoryPage:
        self.page.get_by_role("button", name="Open Menu", exact=False).click()
        self.page.locator(".bm-menu").wait_for(state="visible", timeout=ACTION_WAIT_MS)
        return self

    def click_logout(self) -> None:
        """Open the burger menu and click Logout."""
        from pages.login_page import LoginPage
        self.open_burger_menu()
        self.page.get_by_role("link", name="Logout", exact=False).click()
        self.page.wait_for_load_state("networkidle")

    def click_add_to_cart_for_item(self, item_name: str) -> InventoryPage:
        """Click Add to cart for the inventory item whose name matches item_name."""
        item = self.page.locator(".inventory_item").filter(
            has=self.page.get_by_text(item_name, exact=False)
        )
        btn = item.get_by_role("button", name="Add to cart", exact=False)
        btn.wait_for(state="visible", timeout=ACTION_WAIT_MS)
        btn.click()
        return self

    def click_remove_for_item(self, item_name: str) -> InventoryPage:
        item = self.page.locator(".inventory_item").filter(
            has=self.page.get_by_text(item_name, exact=False)
        )
        btn = item.get_by_role("button", name="Remove", exact=False)
        btn.wait_for(state="visible", timeout=ACTION_WAIT_MS)
        btn.click()
        return self

    def click_cart_icon(self) -> CartPage:
        from pages.cart_page import CartPage
        self.page.locator("[data-test='shopping-cart-link']").click()
        self.page.wait_for_load_state("networkidle")
        return CartPage(self.page)

    def select_sort_option(self, option_value: str) -> InventoryPage:
        """Select a sort option by its value attribute (e.g. 'az', 'za', 'lohi', 'hilo')."""
        self.page.locator("[data-test='product-sort-container']").select_option(option_value)
        self.page.wait_for_load_state("networkidle")
        return self

    # ── state checks ──────────────────────────────────────────────────────────

    def is_on_inventory_page(self) -> bool:
        try:
            self.page.locator(".inventory_list").wait_for(
                state="visible", timeout=ACTION_WAIT_MS
            )
            return True
        except Exception:
            return False

    def get_cart_badge_count(self) -> int:
        badge = self.page.locator("[data-test='shopping-cart-badge']")
        try:
            badge.wait_for(state="visible", timeout=ACTION_WAIT_MS)
        except Exception:
            return 0
        text = badge.inner_text().strip()
        return int(text) if text.isdigit() else 0

    def get_inventory_item_names(self) -> list[str]:
        self.page.locator(".inventory_item").first.wait_for(
            state="visible", timeout=ACTION_WAIT_MS
        )
        return [
            el.inner_text().strip()
            for el in self.page.locator(".inventory_item_name").all()
        ]

    def get_inventory_item_count(self) -> int:
        return len(self.page.locator(".inventory_item").all())

    def is_remove_button_visible_for_item(self, item_name: str) -> bool:
        item = self.page.locator(".inventory_item").filter(
            has=self.page.get_by_text(item_name, exact=False)
        )
        btn = item.get_by_role("button", name="Remove", exact=False)
        try:
            btn.wait_for(state="visible", timeout=ACTION_WAIT_MS)
            return True
        except Exception:
            return False

    def get_item_prices(self) -> list[float]:
        """Return all displayed item prices as floats."""
        self.page.locator(".inventory_item_price").first.wait_for(
            state="visible", timeout=ACTION_WAIT_MS
        )
        prices: list[float] = []
        for el in self.page.locator(".inventory_item_price").all():
            text = el.inner_text().strip().lstrip("$")
            try:
                prices.append(float(text))
            except ValueError:
                pass
        return prices


from pages.cart_page import CartPage  # noqa: E402 — avoid circular at module level
