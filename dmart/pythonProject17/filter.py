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
    time.sleep(2)  # Adding delay to visualize
    location_confirm_button.click()
    print("First delivery location confirmed.")

    # Handle the second location confirmation
    location_confirm_button_2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'pincode-widget_success-cntr-footer__Zo7iY'))
    )
    time.sleep(2)  # Adding delay to visualize
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
    time.sleep(2)  # Adding delay to visualize
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
    time.sleep(2)  # Adding delay to visualize
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

        # Click on the specified button
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'categories-header_listStaticItemLink__nv212'))
            )
            time.sleep(2)  # Adding delay to visualize
            button.click()
            print("First button clicked successfully.")

            # Click on the element with class "all-categories_text__6Xr5l" and text "Dairy"
            try:
                dairy_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='all-categories_text__6Xr5l' and contains(text(),'Dairy')]"))
                )
                time.sleep(2)  # Adding delay to visualize
                dairy_button.click()
                print("Dairy button clicked successfully.")
                print("Test Case Passed: Filter")
            except TimeoutException:
                print("TimeoutException: Dairy button with the specified class name not found.")
            except NoSuchElementException as e:
                print(f"Element not found: {e}")

        except TimeoutException:
            print("TimeoutException: First button with the specified class name not found.")
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
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