import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


# Selenium tests for the Sauce Demo site (https://www.saucedemo.com/).
URL = "https://www.saucedemo.com/"
# Load credentials from environment
load_dotenv()
USERNAME = os.environ.get("SAUCE_USERNAME", "username")
PASSWORD = os.environ.get("SAUCE_PASSWORD", "password")
# Explicit wait timeout to test helpers
TIMEOUT = 10


@pytest.fixture
def driver():
    # Chrome webdriver instance to test
    d = webdriver.Chrome()
    yield d
    d.quit()

def take_screenshot(driver, path):
    # assert the file was created so failures are take screenshot to test output.
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.save_screenshot(path)
    assert os.path.exists(path)


def save_page_source(driver, filename="Webpage_task_11.txt"):
    """Save full page HTML to Test-Se/tests/secretsauce_tests/<filename> and return path.

    This helper is useful for debugging failing tests by storing the rendered
    HTML of the current page for offline inspection.
    """
    path = os.path.join(os.getcwd(), "Test-Se", "tests", "secretsauce_tests", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    return path


def perform_login(driver, username, password):
    driver.get(URL)
    # Navigate to login page and wait until username field is present.
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "user-name")))
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    


def test_positive_login_and_capture(driver):
    # Positive login flow:
    # 1) Open homepage and do basic sanity checks
    driver.get(URL)
    # Validate homepage title and URL
    assert "Swag Labs" in driver.title
    assert driver.current_url.startswith(URL)
    print("Homepage title:", driver.title)
    print("Homepage URL:", driver.current_url)

    # 2) Perform login using helper with credentials
    perform_login(driver, USERNAME, PASSWORD)

    # 3) Verify we've arrived at the inventory page and capture evidence
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("/inventory.html"))
    assert "/inventory.html" in driver.current_url
    screenshot_path = os.path.join(
        os.getcwd(),
        "Test-Se",
        "tests",
        "secretsauce_tests",
        "test_screenshots",
        "secretsauce_valid_login_result.png"
    )
    take_screenshot(driver, screenshot_path)

    # Save page HTML for debugging or reporting
    saved = save_page_source(driver, "Webpage_task_11.txt")
    assert os.path.exists(saved)


def test_negative_login_wrong_password(driver):
    # Negative login flow: attempt login with a wrong password and verify error
    driver.get(URL)
    perform_login(driver, USERNAME, "wrong_password")

    # The login should fail and an error element should appear on the page.
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3[data-test='error']")))
    assert "/inventory.html" not in driver.current_url
    screenshot_path = os.path.join(
        os.getcwd(),
        "Test-Se",
        "tests",
        "secretsauce_tests",
        "test_screenshots",
        "secretsauce_invalid_login_result.png"
    )
    take_screenshot(driver, screenshot_path)
