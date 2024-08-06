import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def get_element_xpath(element):
    tag = element.tag_name
    if element.get_attribute("id"):
        return (tag, "id", element.get_attribute("id"), f'//{tag}[@id=*{element.get_attribute("id")}*]')
    elif element.get_attribute("placeholder"):
        return (tag, "placeholder", element.get_attribute("placeholder"),
                f'//{tag}[@placeholder=*{element.get_attribute("placeholder")}*]')
    elif element.get_attribute("name"):
        return (tag, "name", element.get_attribute("name"), f'//{tag}[@name=*{element.get_attribute("name")}*]')
    elif element.get_attribute("type"):
        return (tag, "type", element.get_attribute("type"), f'//{tag}[@type=*{element.get_attribute("type")}*]')
    else:
        return (tag, "", "", "")


def collect_xpaths(driver):
    elements = driver.find_elements(By.XPATH, "//*")
    xpaths = []

    for elem in elements:
        tag, locator_name, locator_value, xpath = get_element_xpath(elem)
        if locator_name and locator_value:  # Only include elements with the specified attributes
            xpaths.append((tag, locator_name, locator_value, xpath))

    return xpaths


def save_to_csv(data, filename="csv/xpaths_gh.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["name", "LocatorName", "LocatorValue", "LocatorType"])
        for row in data:
            # Escape double quotes in locator value
            locator_value = row[3].replace('""', '')
            locator_value = locator_value.replace('"', '')
            locator_value = locator_value.replace('*', "'")
            writer.writerow([row[0], row[1], locator_value, "XPath"])


# Initialize WebDriver
driver = webdriver.Chrome()

try:
    driver.maximize_window()
    driver.get("https://github.com/")  # Replace with your target URL
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    time.sleep(3)  # Wait for the page to load completely

    xpaths = collect_xpaths(driver)
    save_to_csv(xpaths)
    print("XPaths saved to xpaths.csv")

finally:
    driver.quit()
