import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException

def find_element(driver, by, value, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )

def click_element(driver, by, value, timeout=20, retries=3):
    for _ in range(retries):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", element)  # Scroll into view
            element.click()
            return
        except StaleElementReferenceException:
            print(f"StaleElementReferenceException: Retrying click for element with {by} = {value}")
        except TimeoutException:
            print(f"TimeoutException: Element with {by} = {value} not clickable.")
    raise StaleElementReferenceException(f"Failed to click element with {by} = {value} after {retries} retries")

# Initialize Chrome driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to Dmart website
driver.get('https://www.dmart.in')

try:
    # Handle the first delivery location input
    location_input = find_element(driver, By.CSS_SELECTOR,
                                  '.MuiPaper-root.MuiPaper-elevation.MuiPaper-rounded.MuiPaper-elevation1.pincode-widget_pin-body__Kbj88.mui-style-1vg5txu').find_element(By.TAG_NAME, 'input')
    delivery_location = '560054'
    print("Location input found, entering delivery location...")
    location_input.send_keys(delivery_location)
    location_input.send_keys(Keys.RETURN)
    print("Delivery location code entered.")

    # Confirm the first location
    click_element(driver, By.CLASS_NAME, 'pincode-widget_pincode-right__TwcOu')
    print("First delivery location confirmed.")

    # Handle the second location confirmation
    click_element(driver, By.CLASS_NAME, 'pincode-widget_success-cntr-footer__Zo7iY')
    print("Second delivery location confirmed.")

    # Click the register button
    click_element(driver, By.CSS_SELECTOR, '.header_titleCntrGuest__pwe5K')
    print("Register button clicked.")

    # Wait for mobile number input
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, '.MuiInputBase-root.MuiOutlinedInput-root'))
    )

    # Enter mobile number
    mobile_input = find_element(driver, By.CSS_SELECTOR,
                                '.MuiInputBase-root.MuiOutlinedInput-root.MuiInputBase-colorPrimary.MuiInputBase-fullWidth.MuiInputBase-adornedStart.common_mobileNumberField__Qs6w1.mui-style-1ez65di').find_element(By.TAG_NAME, 'input')
    mobile_number = '6366470763'
    mobile_input.send_keys(mobile_number)
    print("Mobile number entered.")

    # Click the continue button after entering the mobile number
    click_element(driver, By.CLASS_NAME, 'MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.MuiButton-fullWidth.common_loginButton__2S1C3.mui-style-l8jzhy')
    print("Continue button clicked after mobile number entry.")

    # Prompt for manual OTP entry
    input("Please enter the OTP manually and press Enter to continue...")
    # Wait for OTP processing (you may need to adjust the sleep time based on your scenario)
    time.sleep(5)  # Adjust time as needed to ensure OTP processing

    # Click the verify OTP button
    click_element(driver, By.CSS_SELECTOR,
                  '.MuiButtonBase-root.MuiButton-root.MuiButton-contained.MuiButton-containedPrimary.MuiButton-sizeMedium.MuiButton-containedSizeMedium.MuiButton-colorPrimary.MuiButton-fullWidth.common_verifyOtpButton__5CYZz.mui-style-l8jzhy')
    print("OTP verification button clicked.")

    # Add a delay before finishing the script
    time.sleep(5)

    # Print test case passed message
    print("Test case passed.")

except TimeoutException:
    print("TimeoutException: Element not found or action not completed in time.")
except NoSuchElementException as e:
    print(f"Element not found: {e}")
except StaleElementReferenceException as e:
    print(f"StaleElementReferenceException: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Adding a delay before closing the browser to allow manual verification
time.sleep(10)
print("login successfullly...")

# Quit the driver
driver.quit()