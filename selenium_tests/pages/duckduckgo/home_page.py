from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class DuckDuckGoHomePage(BasePage):
    """Page object for the DuckDuckGo home / search page."""

    URL = "https://duckduckgo.com"

    _SEARCH_BOX = (By.NAME, "q")

    # Hamburger / menu button — ordered from most to least stable
    _HAMBURGER_LOCATORS = [
        (By.CSS_SELECTOR, "button[data-testid='sidemenu-button']"),
        (By.XPATH, '//button[normalize-space(.)="Menu"]'),
        (By.XPATH, '/html/body/div[1]/header/div[1]/div[2]/button'),
        (By.XPATH, "//header//button[.//svg]"),
    ]

    _SETTINGS_LINK_LOCATORS = [
        (By.XPATH, '//a[normalize-space(.)="Settings"]'),
        (By.XPATH, '//a[contains(., "Settings")]'),
        (By.XPATH, '//button[normalize-space(.)="Settings"]'),
        (By.LINK_TEXT, "Settings"),
    ]

    def open(self) -> "DuckDuckGoHomePage":
        super().open(self.URL)
        self.wait.until(lambda d: "DuckDuckGo" in d.title)
        return self

    def search(self, query: str) -> "DuckDuckGoHomePage":
        box = self.find(self._SEARCH_BOX)
        box.send_keys(query, Keys.RETURN)
        return self

    def open_menu(self) -> "DuckDuckGoHomePage":
        for locator in self._HAMBURGER_LOCATORS:
            try:
                # Wait until at least one element with this locator is present,
                # then pick the first one that is actually displayed.
                self.wait.until(EC.presence_of_element_located(locator))
                candidates = self.driver.find_elements(*locator)
                for el in candidates:
                    if el.is_displayed() and el.size.get("width", 0) > 0:
                        try:
                            el.click()
                        except Exception:
                            self.driver.execute_script("arguments[0].click();", el)
                        return self
            except Exception:
                continue
        raise RuntimeError("Hamburger / menu button not found.")

    def go_to_settings(self) -> "DuckDuckGoHomePage":
        for locator in self._SETTINGS_LINK_LOCATORS:
            try:
                self.click(locator)
                return self
            except Exception:
                continue
        raise RuntimeError("Settings link not found in the menu.")
