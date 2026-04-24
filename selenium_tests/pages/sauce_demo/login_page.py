from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SauceDemoLoginPage(BasePage):
    """Page object for the Sauce Demo login page."""

    URL = "https://www.saucedemo.com/"

    _USERNAME_FIELD = (By.ID, "user-name")
    _PASSWORD_FIELD = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")

    def open(self) -> "SauceDemoLoginPage":
        super().open(self.URL)
        self.find(self._USERNAME_FIELD)
        return self

    def login(self, username: str, password: str) -> "SauceDemoLoginPage":
        self.type_text(self._USERNAME_FIELD, username)
        self.type_text(self._PASSWORD_FIELD, password)
        self.click(self._LOGIN_BUTTON)
        return self

    def get_error_message(self) -> str:
        return self.wait.until(EC.presence_of_element_located(self._ERROR_MESSAGE)).text

    def is_error_displayed(self) -> bool:
        return self.is_visible(self._ERROR_MESSAGE, timeout=5)
