from selenium import webdriver
import os
from dotenv import load_dotenv

load_dotenv()

# Define the URL and the path to save the screenshot
url = os.getenv('LINK')
save_folder = '../screenshots'
screenshot_filename = 'screenshot.png'

# Create the folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)

# Initialize the WebDriver (using Chrome in this example)
driver = webdriver.Chrome()  # Add executable_path='path_to_chromedriver' if needed

try:
    # Open the webpage
    driver.get(url)
    driver.maximize_window()
    # Save the screenshot
    screenshot_path = os.path.join(save_folder, screenshot_filename)
    driver.save_screenshot(screenshot_path)

    print(f'Screenshot saved at {screenshot_path}')
finally:
    # Close the WebDriver
    driver.quit()
