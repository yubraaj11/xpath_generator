import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

load_dotenv()


def get_full_xpath(element):
    components = []
    child = element

    # Traverse the tree from the element to the <body> tag
    while child.tag_name.lower() != 'body':
        parent = child.find_element(By.XPATH, '..')
        siblings = parent.find_elements(By.XPATH, f"./{child.tag_name}")
        index = siblings.index(child) + 1 if len(siblings) > 1 else ''

        # Add the tag and index to the components
        components.append(f"{child.tag_name}[{index}]" if index else child.tag_name)
        child = parent

    # Add the 'body' tag to the XPath
    components.append('body')
    components.reverse()
    return '/html/' + '/'.join(components)


def get_element_xpath(element):
    tag = element.tag_name
    attributes = ["id", "placeholder", "name", "type"]

    # Check for common attributes
    for attr in attributes:
        attr_value = element.get_attribute(attr)
        if attr_value:
            return tag, attr, attr_value, f"//{tag}[@{attr}='{attr_value}']"

    # Check if element has text content and use it for XPath
    if tag.lower() == 'button':
        text_content = element.text.strip()
        if text_content:
            # Shorten text for XPath to avoid overly specific matches
            truncated_text = text_content if len(text_content) <= 40 else text_content[:40] + '...'
            return tag, "text", truncated_text, f"//{tag}[contains(text(), '{truncated_text}')]"

    # If no attributes or text, generate the full XPath
    full_xpath = get_full_xpath(element)
    return tag, "", "", full_xpath


def collect_xpaths(driver):
    elements = driver.find_elements(By.XPATH, "//body//*")  # Only elements within <body>
    xpaths = [get_element_xpath(elem) for elem in elements]
    return xpaths


def save_to_csv(data, filename="../csv/XPATHS.csv"):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["Tag", "LocatorName", "LocatorValue", "LocatorType"])
            for row in data:
                writer.writerow([row[0], row[2], row[3], "Xpath"])
        print(f"CSV saved to {filename}")
    except Exception as e:
        print(f"Error saving CSV: {e}")


def main():
    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver in your PATH
    try:
        driver.maximize_window()
        driver.get(os.getenv('LINK'))  # Replace with your target URL
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
