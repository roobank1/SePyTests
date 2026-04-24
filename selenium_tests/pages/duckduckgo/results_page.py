from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class DuckDuckGoResultsPage(BasePage):
    """Page object for the DuckDuckGo search results page."""

    _FIRST_RESULT = (By.CSS_SELECTOR, "a[data-testid='result-title-a']")
    _SETTINGS_DROPDOWN = (By.CSS_SELECTOR, ".zcm__link.dropdown__button.js-dropdown-button")

    def first_result_title(self) -> str:
        element = self.wait.until(EC.presence_of_element_located(self._FIRST_RESULT))
        return element.text

    def click_first_result(self) -> str:
        element = self.wait.until(EC.element_to_be_clickable(self._FIRST_RESULT))
        title = element.text
        element.click()
        return title

    def click_settings_dropdown(self) -> "DuckDuckGoResultsPage":
        self.click(self._SETTINGS_DROPDOWN)
        return self
