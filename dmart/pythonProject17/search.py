import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Initialize Chrome driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to Dmart website
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
except NoSuchElementException as e:
    print(f"Element not found: {e}")

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

    # Check if search results are present
    results = driver.find_elements(By.CLASS_NAME, 'search-landing_searchMainContainer__vhRYB')
    print(f"Number of search results found: {len(results)}")

    if len(results) > 0:
        print("Test Passed: Search results are displayed.")
    else:
        print("Test Failed: No search results found.")
except NoSuchElementException as e:
    print(f"Element not found: {e}")
except TimeoutException:
    print("TimeoutException: No search results found within the given time period.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Adding a delay before closing the browser to allow manual verification
time.sleep(10)

# Quit the driver
driver.quit()
