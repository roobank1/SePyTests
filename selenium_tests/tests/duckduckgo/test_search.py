import os

from pages.duckduckgo.home_page import DuckDuckGoHomePage
from pages.duckduckgo.results_page import DuckDuckGoResultsPage

SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")


def test_click_first_result(driver):
    """Search and click the first organic result; URL should change."""
    home = DuckDuckGoHomePage(driver)
    home.open()
    home.search("hey duckduckgo")

    results = DuckDuckGoResultsPage(driver)
    clicked_title = results.click_first_result()

    assert driver.current_url != DuckDuckGoHomePage.URL
    home.take_screenshot(os.path.join(SCREENSHOTS_DIR, "click_first_result.png"))
    print(f"Clicked result: {clicked_title}")


def test_settings_dropdown(driver):
    """Search and open the settings/more-options dropdown on the results page."""
    home = DuckDuckGoHomePage(driver)
    home.open()
    home.search("hi duckduckgo")

    results = DuckDuckGoResultsPage(driver)
    results.click_settings_dropdown()

    results.take_screenshot(os.path.join(SCREENSHOTS_DIR, "settings_dropdown.png"))


def test_basic_navigation(driver):
    """Open the hamburger menu, navigate to Settings, then go back."""
    home = DuckDuckGoHomePage(driver)
    home.open()

    assert "DuckDuckGo" in driver.title

    home.open_menu()
    home.go_to_settings()

    driver.back()
