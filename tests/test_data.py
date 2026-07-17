from __future__ import annotations

import os

# ── credentials ───────────────────────────────────────────────────────────────
VALID_USERNAME: str = os.environ.get("TEST_USERNAME", "standard_user")
VALID_PASSWORD: str = os.environ.get("TEST_PASSWORD", "secret_sauce")

LOCKED_USERNAME: str = "locked_out_user"
LOCKED_PASSWORD: str = "secret_sauce"

INVALID_USERNAME: str = "nonexistent_user"
INVALID_PASSWORD: str = "wrong_password"

# ── URLs ──────────────────────────────────────────────────────────────────────
APP_URL: str = os.environ.get("APP_URL", "https://www.saucedemo.com")
INVENTORY_URL: str = f"{APP_URL}/inventory.html"
CART_URL: str = f"{APP_URL}/cart.html"
CHECKOUT_ONE_URL: str = f"{APP_URL}/checkout-step-one.html"
CHECKOUT_TWO_URL: str = f"{APP_URL}/checkout-step-two.html"
CHECKOUT_COMPLETE_URL: str = f"{APP_URL}/checkout-complete.html"

# ── inventory ─────────────────────────────────────────────────────────────────
EXPECTED_PRODUCT_COUNT: int = 6

PRODUCT_BACKPACK: str = "Sauce Labs Backpack"
PRODUCT_BIKE_LIGHT: str = "Sauce Labs Bike Light"
PRODUCT_BOLT_SHIRT: str = "Sauce Labs Bolt T-Shirt"
PRODUCT_FLEECE_JACKET: str = "Sauce Labs Fleece Jacket"
PRODUCT_ONESIE: str = "Sauce Labs Onesie"
PRODUCT_RED_SHIRT: str = "Test.allTheThings() T-Shirt (Red)"

ALL_PRODUCTS: list[str] = [
    PRODUCT_BACKPACK,
    PRODUCT_BIKE_LIGHT,
    PRODUCT_BOLT_SHIRT,
    PRODUCT_FLEECE_JACKET,
    PRODUCT_ONESIE,
    PRODUCT_RED_SHIRT,
]

# ── checkout ──────────────────────────────────────────────────────────────────
CHECKOUT_FIRST_NAME: str = "Jane"
CHECKOUT_LAST_NAME: str = "Smith"
CHECKOUT_POSTAL_CODE: str = "10001"

# ── error messages (SauceDemo specific) ───────────────────────────────────────
ERROR_LOCKED_OUT: str = "Sorry, this user has been locked out."
ERROR_INVALID_CREDENTIALS: str = "Username and password do not match"
ERROR_USERNAME_REQUIRED: str = "Username is required"
ERROR_PASSWORD_REQUIRED: str = "Password is required"
ERROR_FIRST_NAME_REQUIRED: str = "First Name is required"
ERROR_LAST_NAME_REQUIRED: str = "Last Name is required"
ERROR_POSTAL_CODE_REQUIRED: str = "Postal Code is required"

# ── misc ──────────────────────────────────────────────────────────────────────
MAX_LOOP_ITERATIONS: int = 20
ORDER_COMPLETE_HEADER: str = "Thank you for your order!"
