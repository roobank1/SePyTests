from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class SauceDemoInventoryPage(BasePage):
    """Page object for the Sauce Demo product inventory page."""

    _INVENTORY_CONTAINER = (By.ID, "inventory_container")
    _INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")

    def is_loaded(self) -> bool:
        try:
            self.wait.until(EC.url_contains("/inventory.html"))
            self.wait.until(EC.visibility_of_element_located(self._INVENTORY_CONTAINER))
            return True
        except Exception:
            return False

    def item_count(self) -> int:
        items = self.driver.find_elements(*self._INVENTORY_ITEMS)
        return len(items)
