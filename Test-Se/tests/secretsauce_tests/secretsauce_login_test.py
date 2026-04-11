import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv


URL = "https://www.saucedemo.com/"
# Load credentials from .env (optional). Defaults kept for convenience.
load_dotenv()
USERNAME = os.environ.get("SAUCE_USERNAME", "standard_user")
PASSWORD = os.environ.get("SAUCE_PASSWORD", "secret_sauce")
TIMEOUT = 10


@pytest.fixture
def driver():
    d = webdriver.Chrome()
    yield d
    d.quit()

def take_screenshot(driver, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    driver.save_screenshot(path)
    assert os.path.exists(path)


def perform_login(driver, username, password):
    driver.get(URL)
    # wait for username input
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.ID, "user-name")))
    driver.find_element(By.ID, "user-name").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    


def test_positive_login_and_capture(driver):
    # Home page
    driver.get(URL)
    assert "Swag Labs" in driver.title
    assert driver.current_url.startswith(URL)

    # Login with valid credentials
    perform_login(driver, USERNAME, PASSWORD)

    # After login we expect inventory page
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
    # Save page source
    # saved = save_page_source(driver, "Webpage_task_11.txt")
    # assert os.path.exists(saved)


def test_negative_login_wrong_password(driver):
    driver.get(URL)
    perform_login(driver, USERNAME, "wrong_password")

    # Should remain on login page and show error
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
