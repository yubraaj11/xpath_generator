import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from utils.text_preprocessing import format_, format_text

load_dotenv()

driver = webdriver.Chrome()  # Make sure you have the ChromeDriver in your PATH


def get_element_xpath(element):
    tag = element.tag_name
    attributes = ["id", "placeholder", "name"]

    # Check for common attributes
    for attr in attributes:
        attr_value = element.get_attribute(attr)
        if attr_value:
            attr_val = format_text(attr_value)
            return tag, attr, attr_val, f"//{tag}[@{attr}='{attr_value}']"

    if tag.lower() == 'button' or tag.lower() == 'a':
        # Attempt to retrieve only the direct text node content within the button or anchor
        script = """return Array.from(arguments[0].childNodes).filter(node => 
                    node.nodeType === Node.TEXT_NODE).map(node => node.textContent.trim()).join(' ');"""
        direct_text = driver.execute_script(script, element).strip()

        if direct_text:
            # Shorten text for XPath to avoid overly specific matches
            truncated_text = direct_text if len(direct_text) <= 20 else direct_text[:20] + '...'
            truncated_text = format_(truncated_text)
            return tag, "text", truncated_text, f"//{tag}[contains(text(), '{truncated_text}')]"

    # Return None if no suitable locator is found
    return None


def collect_xpaths(driver):
    elements = driver.find_elements(By.XPATH, "//body//*")  # Only elements within <body>
    xpaths = [get_element_xpath(elem) for elem in elements]
    # Filter out None values if no suitable locator was found
    xpaths = [xpath for xpath in xpaths if xpath is not None]
    return xpaths


def save_to_csv(data, filename="../csv/RATIONAL_LOGIN_UI.csv"):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["LocatorName", "LocatorValue", "LocatorType"])
            for row in data:
                writer.writerow([row[2], row[3], "Xpath"])
        print(f"CSV saved to {filename}")
    except Exception as e:
        print(f"Error saving CSV: {e}")


def main():
    try:
        driver.maximize_window()
        driver.get(os.getenv('RATIONAL'))  # Replace with your target URL
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)  # Wait for the page to load completely

        xpaths = collect_xpaths(driver)

        if not xpaths:
            print("No elements found or XPaths generated.")

        save_to_csv(xpaths)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()