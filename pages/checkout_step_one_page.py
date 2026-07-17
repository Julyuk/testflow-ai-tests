from __future__ import annotations

import os
from playwright.sync_api import Page

APP_URL = os.environ.get("APP_URL", "https://www.saucedemo.com")
CHECKOUT_ONE_URL = f"{APP_URL}/checkout-step-one.html"

ACTION_WAIT_MS = 5_000


class CheckoutStepOnePage:
    """Page Object for SauceDemo checkout step one (delivery info)."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def __repr__(self) -> str:
        return f"CheckoutStepOnePage(url={self.page.url!r})"

    # ── navigation ────────────────────────────────────────────────────────────

    def navigate(self) -> CheckoutStepOnePage:
        self.page.goto(CHECKOUT_ONE_URL)
        self.page.wait_for_load_state("networkidle")
        self.page.locator("[data-test='firstName']").wait_for(state="visible")
        return self

    # ── actions ───────────────────────────────────────────────────────────────

    def fill_first_name(self, value: str) -> CheckoutStepOnePage:
        self.page.locator("[data-test='firstName']").fill(value)
        return self

    def fill_last_name(self, value: str) -> CheckoutStepOnePage:
        self.page.locator("[data-test='lastName']").fill(value)
        return self

    def fill_postal_code(self, value: str) -> CheckoutStepOnePage:
        self.page.locator("[data-test='postalCode']").fill(value)
        return self

    def click_continue(self) -> CheckoutStepTwoPage:
        from pages.checkout_step_two_page import CheckoutStepTwoPage
        self.page.locator("[data-test='continue']").click()
        self.page.wait_for_load_state("networkidle")
        return CheckoutStepTwoPage(self.page)

    def click_continue_expecting_error(self) -> CheckoutStepOnePage:
        self.page.locator("[data-test='continue']").click()
        return self

    def fill_delivery_info(
        self,
        first_name: str,
        last_name: str,
        postal_code: str,
    ) -> CheckoutStepOnePage:
        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_postal_code(postal_code)
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

    def is_on_step_one(self) -> bool:
        try:
            self.page.locator("[data-test='firstName']").wait_for(
                state="visible", timeout=ACTION_WAIT_MS
            )
            return True
        except Exception:
            return False


from pages.checkout_step_two_page import CheckoutStepTwoPage  # noqa: E402
