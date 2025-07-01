import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

# Initialize Chrome driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def test_add_and_remove_item_from_cart_dmart():
    driver.get('https://www.dmart.in')

    try:
        # Handle the first delivery location input
        location_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.pincode-widget_pin-body__Kbj88.mui-style-1vg5txu'))
        )
        location_input = location_container.find_element(By.TAG_NAME, 'input')
        delivery_location = '560054'  # Specify your delivery location here
        print("Location input found, entering delivery location...")
        location_input.send_keys(delivery_location)
        location_input.send_keys(Keys.RETURN)
        print("Delivery location code entered.")

        # Confirm the first location
        location_confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'pincode-widget_pincode-right__TwcOu'))
        )
        location_confirm_button.click()
        print("First delivery location confirmed.")

        # Handle the second location confirmation
        location_confirm_button_2 = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'pincode-widget_success-cntr-footer__Zo7iY'))
        )
        location_confirm_button_2.click()
        print("Second delivery location confirmed.")
    except TimeoutException:
        print("TimeoutException: Delivery location input or confirm button not found.")
        driver.quit()
        return
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        driver.quit()
        return

    # Handle potential pop-ups (if any, otherwise this part can be skipped)
    try:
        close_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'popup-close'))
        )
        close_button.click()
        print("Login popup closed successfully.")
    except TimeoutException:
        print("Login popup did not appear or could not be closed.")
    except NoSuchElementException:
        print("Close button not found.")

    # Find the search bar and perform a search
    try:
        search_bar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'search_searchInput__YlEPv'))
        )
        search_term = 'groceries'  # Specify your search term here
        print("Search bar found, entering search term...")
        search_bar.send_keys(search_term)
        search_bar.send_keys(Keys.RETURN)

        # Wait for search results to load
        print("Waiting for search results to load...")
        WebDriverWait(driver, 40).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'search-landing_searchMainContainer__vhRYB'))
        )
        print("Search results loaded.")
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        driver.quit()
        return
    except TimeoutException:
        print("TimeoutException: No search results found within the given time period.")
        driver.quit()
        return

    try:
        # Click on the first item in the search results
        first_item = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'vertical-card_section-top__XyqW3'))
        )
        first_item.click()
        print("First item clicked.")
    except TimeoutException:
        print("First item not clickable or not found.")
        driver.quit()
        return
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        driver.quit()
        return
    except ElementClickInterceptedException as e:
        print(f"ElementClickInterceptedException: {e}")
        driver.quit()
        return

    try:
        # Wait for the product page to load
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.addToCart_component_action-container__WnZyd'))
        )
        print("Product page loaded.")
    except TimeoutException:
        print("Product page did not load in time.")
        driver.quit()
        return

    try:
        # Add the item to the cart
        add_to_cart_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.addToCart_component_action-container__WnZyd'))
        )
        add_to_cart_button.click()
        print("Item added to cart.")

        # Adding a delay to ensure the item is added to the cart
        time.sleep(5)
    except TimeoutException:
        print("Add to Cart button not clickable or not found.")
        driver.quit()
        return

    try:
        # Click on the cart icon to view the cart
        cart_icon = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.header_countCntr___kHcR.mui-style-1yxmbwk'))
        )
        cart_icon.click()
        print("Cart icon clicked.")
    except TimeoutException:
        print("Cart icon not clickable or not found.")
        driver.quit()
        return
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except ElementClickInterceptedException:
        print("Element click intercepted.")

    try:
        # Wait for the cart page to load and verify the item is in the cart
        WebDriverWait(driver, 60).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'mini-cart_action__nVlHO'))
        )
        print("Test Passed: Item is in the cart.")
    except TimeoutException:
        print("Cart page did not load in time or no items found in the cart.")
    except NoSuchElementException:
        print("Cart item list element not found.")


    # Now, remove the item from the cart
    try:
        view_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'mini-cart_action__nVlHO'))
        )
        view_button.click()
        print("view button clicked.")

        # Adding a delay to ensure the item is removed from the cart
        time.sleep(5)
    except TimeoutException:
        print("view button not clickable or not found.")
        driver.quit()
        return
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        driver.quit()
        return
    try:
        button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.cart-web_remove__5aFVR'))
        )
        button.click()
        print("remove button clicked.")

        # Adding a delay to ensure the item is removed from the cart
        time.sleep(5)
    except TimeoutException:
        print("remove button not clickable or not found.")
        driver.quit()
        return
    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        driver.quit()
        return

    try:
        # Verify the cart is empty
        empty_cart_message = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'cart-empty_empty_state__xFcW0'))
        )
        if empty_cart_message:
            print("Test Passed: Item removed from the cart successfully.")
        else:
            print("Test Failed: Cart is not empty.")
    except TimeoutException:
        print("TimeoutException: Empty cart message not found.")
    except NoSuchElementException:
        print("Empty cart message element not found.")

    print("Test completed. Closing the browser...")
    driver.quit()

# Run the test case
test_add_and_remove_item_from_cart_dmart()
