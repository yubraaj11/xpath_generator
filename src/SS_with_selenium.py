from selenium import webdriver
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Define the URL and the path to save the screenshot
url = os.getenv('DB')
save_folder = '../screenshots'
screenshot_filename = 'screenshot_2.png'

# Create the folder if it doesn't exist
os.makedirs(save_folder, exist_ok=True)

# Initialize the WebDriver (using Chrome in this example)
  # Add executable_path='path_to_chromedriver' if needed


def take_ss(file_name, driver):
    # Save the screenshot
    screenshot_path = os.path.join(save_folder, file_name)
    driver.save_screenshot(screenshot_path)

    print(f'Screenshot saved at {screenshot_path}')


if __name__ == "__main__":
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        driver.maximize_window()

        ss_file_name = ['ss_1.png', 'ss_2.png']
        for file in ss_file_name:
            time.sleep(4)
            take_ss(file, driver=driver)
    finally:
        driver.quit()