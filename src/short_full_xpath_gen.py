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

    for attr in attributes:
        attr_value = element.get_attribute(attr)
        if attr_value:
            return tag, attr, attr_value, f"//{tag}[@{attr}='{attr_value}']"

    # If no attributes are found, generate the full XPath
    full_xpath = get_full_xpath(element)
    return tag, "", "", full_xpath


def collect_xpaths(driver):
    elements = driver.find_elements(By.XPATH, "//body//*")  # Only elements within <body>
    xpaths = [
        get_element_xpath(elem)
        for elem in elements
    ]
    return xpaths


location_path = "../csv/short_full_xpaths.csv"

def save_to_csv(data, filename=location_path):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Tag","LocatorName", "LocatorValue", "LocatorType"])
        for row in data:
            writer.writerow([row[0], row[2], row[3], "XPath"])


def main():
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get(os.getenv("LINK"))  # Replace with your target URL
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)  # Wait for the page to load completely

        xpaths = collect_xpaths(driver)
        save_to_csv(xpaths)
        print("XPaths saved to ../csv/short_full_xpaths.csv")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
