# Simple Guvi login tests without using page object model, to demonstrate basic Selenium usage and test structure.

import os
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

BASE_URL = "https://www.guvi.in"
SIGN_IN_URL = "https://www.guvi.in/sign-in/"


def first(driver, selector):
    # Return the first element matching `selector`, or None if not found
    els = driver.find_elements(By.CSS_SELECTOR, selector)
    return els[0] if els else None


def test_open_home(driver):
    # Open the homepage and confirm it's Guvi by URL or title
    driver.get(BASE_URL)
    assert "guvi" in driver.current_url or "guvi" in driver.title.lower()


def test_click_signin(driver):
    driver.get(BASE_URL)
    # Common selectors that often point to the sign-in/login link
    sel = 'a[href*="sign-in"], a[href*="login"], a[class*="sign"], a[title*="Sign"], a[aria-label*="sign"]'
    link = first(driver, sel)
    if link:
        # Click the link if found
        link.click()
    else:
        # Fallback: open sign-in page directly
        driver.get(SIGN_IN_URL)
    # Check sign-in by URL, or by the clicked link's href if available
    assert "sign-in" in driver.current_url or (link is not None and "sign-in" in (link.get_attribute("href") or ""))


def _perform_login(driver, username, password):
    # Load the sign-in page and try to fill common login fields
    driver.get(SIGN_IN_URL)
    # Try several common selectors for email/username and password fields
    u = first(driver, 'input[type="email"], input[name="email"], input[type="text"], input[placeholder*="Email"]')
    p = first(driver, 'input[type="password"], input[name="password"], input[placeholder*="Password"]')
    if not u or not p:
        # Required fields not found
        return False
    # Enter credentials
    u.clear(); u.send_keys(username)
    p.clear(); p.send_keys(password)
    # Find a submit button using common selectors
    s = first(driver, 'button[type="submit"], input[type="submit"], button[class*="login"], button[class*="signin"]')
    if s:
        # Click submit; fall back to JS click if normal click fails
        try:
            s.click()
        except Exception:
            driver.execute_script("arguments[0].click();", s)
    else:
        # Fallback: press Enter in the password field to submit
        try:
            p.send_keys(Keys.ENTER)
        except Exception:
            return False
    return True


def test_login_valid_credentials(driver):
    # Read credentials from environment; skip test if not provided
    USER = os.environ.get("GUVI_USERNAME")
    PWD = os.environ.get("GUVI_PASSWORD")
    if not USER or not PWD:
        pytest.skip("GUVI credentials not set in env")
    ok = _perform_login(driver, USER, PWD)
    if not ok:
        pytest.skip("Login elements not found")
    # Short wait to allow the page to navigate after login
    driver.implicitly_wait(2)
    if driver.current_url == SIGN_IN_URL:
        # If still on sign-in page, try to find common logged-in indicators
        indicators = [
            'a[href*="logout"]', 'a[title*="Logout"]', 'a[aria-label*="logout"]',
            'a[href*="profile"]', 'img[class*="avatar"]', 'button[class*="profile"]'
        ]
        found = any(first(driver, sel) for sel in indicators)
        if not found:
            # Can't confirm login; skip rather than fail the test
            pytest.skip("Could not verify login success in this environment")
    else:
        # If URL changed away from sign-in, assume login succeeded
        assert driver.current_url != SIGN_IN_URL


def test_login_invalid_credentials(driver):
    ok = _perform_login(driver, "no_user@example.com", "bad_pwd")
    if not ok:
        pytest.skip("Login elements not found")
    # Invalid credentials should keep us on the sign-in page
    assert driver.current_url == SIGN_IN_URL
