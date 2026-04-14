from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
import time
from selenium.common.exceptions import TimeoutException

URL = "https://www.duckduckgo.com/"


def click_with_fallback(driver, locator, timeout=5):
	try:
		elem = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
	except TimeoutException:
		return False
	try:
		elem.click()
		return True
	except Exception:
		try:
			driver.execute_script("arguments[0].click();", elem)
			return True
		except Exception:
			return False


def test_basic_navigation(driver):
	# 1) Open DuckDuckGo
	driver.get(URL)
	WebDriverWait(driver, 10).until(EC.title_contains("DuckDuckGo"))
	time.sleep(3)

	# 2) Open hamburger/menu using provided XPath
	hamburger_locator = (By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/button/svg')
	click_with_fallback(driver, hamburger_locator, timeout=5)
	time.sleep(3)

	# 3) Click Settings from the menu
	settings_locators = [
		(By.XPATH, '//a[normalize-space(.)="Settings"]'),
		(By.XPATH, '//a[contains(., "Settings")]'),
		(By.XPATH, '//button[normalize-space(.)="Settings"]'),
	]
	for loc in settings_locators:
		if click_with_fallback(driver, loc, timeout=5):
			break
	time.sleep(3)

	# 4) Navigate back
	driver.back()
	time.sleep(3)


@pytest.fixture
def driver():
	d = webdriver.Chrome()
	yield d
	d.quit()
