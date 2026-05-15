import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


def pytest_addoption(parser):
	parser.addoption(
		"--browser",
		action="store",
		default="chrome",
		help="Browser to run tests against: chrome (default) | firefox | edge",
	)
	parser.addoption(
		"--headless",
		action="store_true",
		default=False,
		help="Run the browser in headless mode",
	)


@pytest.fixture(scope="function")
def driver(request):
	browser = request.config.getoption("--browser").lower()
	headless = request.config.getoption("--headless")

	# Load environment variables from selenium_tests/.env.
	env_path = os.path.join(os.path.dirname(__file__), "selenium_tests", ".env")
	load_dotenv(env_path)

	if browser == "chrome":
		options = ChromeOptions()
		if headless:
			options.add_argument("--headless=new")
		options.add_argument("--no-sandbox")
		options.add_argument("--disable-dev-shm-usage")
		options.add_argument("--disable-extensions")
		driver_instance = webdriver.Chrome(options=options)

	elif browser == "firefox":
		from selenium.webdriver.firefox.options import Options as FirefoxOptions

		options = FirefoxOptions()
		if headless:
			options.add_argument("--headless")
		driver_instance = webdriver.Firefox(options=options)

	elif browser == "edge":
		from selenium.webdriver.edge.options import Options as EdgeOptions

		options = EdgeOptions()
		if headless:
			options.add_argument("--headless")
		driver_instance = webdriver.Edge(options=options)

	else:
		raise ValueError(f"Unsupported browser: '{browser}'. Choose chrome, firefox, or edge.")

	driver_instance.maximize_window()
	driver_instance.implicitly_wait(5)
	yield driver_instance
	driver_instance.quit()