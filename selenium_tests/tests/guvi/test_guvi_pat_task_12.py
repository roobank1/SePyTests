from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


BASE_URL = "https://www.guvi.in/"


def test_guvi_dynamic_xpath_pat_task_12(driver):
	driver.get(BASE_URL)
	WebDriverWait(driver, 15).until(
		lambda d: d.execute_script("return document.readyState") == "complete"
	)
	print("Step 0: Opened GUVI home page")

	# Pick one menu item from the top bar (Practice).
	target_anchor = driver.find_element(
		By.XPATH,
		"(//a[contains(normalize-space(), 'Practice')])[1]"
	)
	print("Step 1: Found menu item -> Practice")

	# Find parent of this element.
	parent_element = target_anchor.find_element(By.XPATH, "./parent::*")
	assert parent_element is not None
	print("Step 2: Found parent element")

	# From the parent, find the first child element.
	first_child = parent_element.find_element(By.XPATH, "./*[1]")
	assert first_child is not None
	print("Step 3: Found first child of parent")

	# Find the second sibling (if present).
	second_sibling = parent_element.find_elements(By.XPATH, "./following-sibling::*[2]")
	assert len(second_sibling) in (0, 1)
	print(f"Step 4: Checked second sibling -> found {len(second_sibling)}")

	# Find parent element of any element that has href attribute.
	href_element_parent = driver.find_element(By.XPATH, "(//*[@href])[1]/..")
	assert href_element_parent is not None
	print("Step 5: Found parent of first href element")

	# Find all ancestor elements.
	ancestors = parent_element.find_elements(By.XPATH, "./ancestor::*")
	assert len(ancestors) > 0
	print(f"Step 6: Ancestors count -> {len(ancestors)}")

	# Find all following siblings.
	following_siblings = parent_element.find_elements(By.XPATH, "./following-sibling::*")
	assert isinstance(following_siblings, list)
	print(f"Step 7: Following siblings count -> {len(following_siblings)}")

	# Find all preceding elements.
	preceding_elements = parent_element.find_elements(By.XPATH, "./preceding::*")
	assert len(preceding_elements) > 0
	print(f"Step 8: Preceding elements count -> {len(preceding_elements)}")
