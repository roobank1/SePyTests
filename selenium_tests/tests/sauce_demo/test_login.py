import os

import pytest
from dotenv import load_dotenv

from pages.sauce_demo.login_page import SauceDemoLoginPage
from pages.sauce_demo.inventory_page import SauceDemoInventoryPage

load_dotenv()

USERNAME = os.environ.get("SAUCE_USERNAME", "username")
PASSWORD = os.environ.get("SAUCE_PASSWORD", "password")

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


def test_valid_login(driver):
    """Valid credentials should land on the inventory page."""
    login_page = SauceDemoLoginPage(driver)
    login_page.open()

    assert "Swag Labs" in driver.title
    assert driver.current_url.startswith(SauceDemoLoginPage.URL)

    login_page.login(USERNAME, PASSWORD)

    inventory = SauceDemoInventoryPage(driver)
    assert inventory.is_loaded(), "Inventory page did not load after valid login."

    login_page.take_screenshot(os.path.join(SCREENSHOTS_DIR, "valid_login.png"))


def test_invalid_password(driver):
    """Wrong password should show an error and stay on the login page."""
    login_page = SauceDemoLoginPage(driver)
    login_page.open()

    login_page.login(USERNAME, "wrong_password")

    assert login_page.is_error_displayed(), "Expected an error message for invalid credentials."
    assert "/inventory.html" not in driver.current_url

    login_page.take_screenshot(os.path.join(SCREENSHOTS_DIR, "invalid_login.png"))


def test_empty_credentials(driver):
    """Submitting empty credentials should show a validation error."""
    login_page = SauceDemoLoginPage(driver)
    login_page.open()

    login_page.login("", "")

    assert login_page.is_error_displayed(), "Expected an error message for empty credentials."
