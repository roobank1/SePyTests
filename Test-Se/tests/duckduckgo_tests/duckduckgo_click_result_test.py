from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pytest


URL = "https://duckduckgo.com"
SEARCH_TEXT = "hey duckduckgo"
TIMEOUT = 5


# ---------- Fixtures ----------
@pytest.fixture
def driver():
    d = webdriver.Chrome()
    yield d
    d.quit()


# ---------- Helper Functions ----------
def perform_search(driver, text):
    search_box = WebDriverWait(driver, TIMEOUT).until(
        EC.presence_of_element_located((By.NAME, "q"))
    )
    search_box.send_keys(text, Keys.RETURN)


def click_first_result(driver):
    element = WebDriverWait(driver, TIMEOUT).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[data-testid='result-title-a']"))
    )
    text = element.text  # capture before click
    element.click()
    return text


def click_with_fallback(driver, locator):
    try:
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element
    except Exception:
        element = WebDriverWait(driver, TIMEOUT).until(
            EC.presence_of_element_located(locator)
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.execute_script("arguments[0].click();", element)
        return element


def take_screenshot(driver, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.save_screenshot(path)
    assert os.path.exists(path)


# ---------- Test 1: Click First Result ----------
def test_click_first_result(driver):
    driver.get(URL)

    perform_search(driver, SEARCH_TEXT)

    clicked_text = click_first_result(driver)

    WebDriverWait(driver, TIMEOUT).until(EC.url_changes(URL))

    screenshot_path = os.path.join(
        os.getcwd(),
        "Test-Se",
        "tests",
        "duckduckgo_tests",
        "test_screenshots",
        "duckduckgo_click_first_result.png"
    )
    take_screenshot(driver, screenshot_path)

    print("Clicked:", clicked_text)


# ---------- Test 2: Click Settings Dropdown ----------
def test_result_settings_click(driver):
    driver.get(URL)

    perform_search(driver, "hi duckduckgo")

    dropdown_locator = (
        By.CSS_SELECTOR,
        ".zcm__link.dropdown__button.js-dropdown-button",
    )

    click_with_fallback(driver, dropdown_locator)

    screenshot_path = os.path.join(
        os.getcwd(),
        "Test-Se",
        "tests",
        "duckduckgo_tests",
        "test_screenshots",
        "duckduckgo_click_result_settings.png"
    )
    take_screenshot(driver, screenshot_path)