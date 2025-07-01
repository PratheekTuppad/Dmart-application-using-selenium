from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

# Initialize Chrome driver
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# Navigate to DMart website
driver.get('https://www.dmart.in')

# Get the actual title
actual_title = driver.title
print(f"Actual Title: {actual_title}")

# Define the expected title
expected_title = "Daily Offers, Daily Discounts on DMart Ready"

# Verify the title
if actual_title == expected_title:
    print("Test Passed: Title is correct.")
else:
    print("Test Failed: Title is incorrect.")

# Close the browser
driver.quit()