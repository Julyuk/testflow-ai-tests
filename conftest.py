from __future__ import annotations

import os
import pytest
from playwright.sync_api import sync_playwright, Page

_BROWSER_ARGS = [
    "--no-sandbox", "--disable-setuid-sandbox",
    "--disable-dev-shm-usage", "--disable-gpu",
    "--no-zygote", "--disable-extensions",
]


@pytest.fixture
def browser():
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=_BROWSER_ARGS, timeout=30_000)
        yield b
        b.close()


@pytest.fixture
def page(browser):
    ctx = browser.new_context(ignore_https_errors=True)
    pg = ctx.new_page()
    pg.set_default_timeout(20_000)
    pg.set_default_navigation_timeout(30_000)
    yield pg
    ctx.close()


@pytest.fixture(autouse=True)
def screenshot_on_failure(page: Page, request):
    """Capture a screenshot automatically when a test fails."""
    yield
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)
        safe_name = request.node.name.replace("/", "_").replace("::", "__")
        path = f"{screenshots_dir}/{safe_name}.png"
        try:
            page.screenshot(path=path, full_page=True)
        except Exception:
            pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture
def logged_in_page(page: Page):
    """Navigate to SauceDemo and log in with standard_user credentials."""
    from pages.login_page import LoginPage
    return (
        LoginPage(page)
        .navigate()
        .login(
            os.environ.get("TEST_USERNAME", "standard_user"),
            os.environ.get("TEST_PASSWORD", "secret_sauce"),
        )
    )
