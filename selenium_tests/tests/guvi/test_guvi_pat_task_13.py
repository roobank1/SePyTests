from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://jqueryui.com/droppable/"

def test_drag_white_box_into_yellow_box(driver):
    # Open the page.
    driver.get(URL)

    # Switch into the demo iframe.
    frame = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.demo-frame"))
    )
    driver.switch_to.frame(frame)

    # Find the white draggable box and yellow drop box.
    white = driver.find_element(By.ID, "draggable")
    yellow = driver.find_element(By.ID, "droppable")

    # Drag the white box to the center of the yellow box using JavaScript.
    driver.execute_script(
        """
        const white = arguments[0];
        const yellow = arguments[1];

        function fire(el, type, x, y) {
            const ev = new MouseEvent(type, {
                bubbles: true,
                cancelable: true,
                view: window,
                clientX: x,
                clientY: y
            });
            el.dispatchEvent(ev);
        }

        const w = white.getBoundingClientRect();
        const y = yellow.getBoundingClientRect();

        const startX = w.left + w.width / 2;
        const startY = w.top + w.height / 2;
        const endX = y.left + y.width / 2;
        const endY = y.top + y.height / 2;

        fire(white, "mousedown", startX, startY);
        fire(white, "mousemove", endX, endY);
        fire(yellow, "mouseup", endX, endY);
        """,
        white,
        yellow,
    )

    # Check the result.
    text = yellow.find_element(By.TAG_NAME, "p").text
    print("Positive result:", text)
    assert text == "Dropped!"

def test_drag_white_box_outside_yellow_box(driver):
    # Open the page.
    driver.get(URL)

    # Switch into the demo iframe.
    frame = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.demo-frame"))
    )
    driver.switch_to.frame(frame)

    # Find the white draggable box and yellow drop box.
    white = driver.find_element(By.ID, "draggable")
    yellow = driver.find_element(By.ID, "droppable")

    # Move the white box just a little to the right, not onto the yellow box.
    driver.execute_script(
        """
        const white = arguments[0];

        function fire(el, type, x, y) {
            const ev = new MouseEvent(type, {
                bubbles: true,
                cancelable: true,
                view: window,
                clientX: x,
                clientY: y
            });
            el.dispatchEvent(ev);
        }

        const w = white.getBoundingClientRect();
        const startX = w.left + w.width / 2;
        const startY = w.top + w.height / 2;
        const endX = startX + 20;
        const endY = startY;

        fire(white, "mousedown", startX, startY);
        fire(white, "mousemove", endX, endY);
        fire(white, "mouseup", endX, endY);
        """,
        white,
    )

    # Check the result.
    text = yellow.find_element(By.TAG_NAME, "p").text
    print("Negative result:", text)
    assert text != "Dropped!"
