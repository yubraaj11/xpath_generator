import csv
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_element_xpath(element):
    tag = element.tag_name
    attributes = ["id", "placeholder", "name", "type"]

    for attr in attributes:
        attr_value = element.get_attribute(attr)
        if attr_value:
            return tag, attr, attr_value, f"//{tag}[@{attr}='{attr_value}']"

    return tag, "", "", ""

def collect_xpaths(driver):
    elements = driver.find_elements(By.XPATH, "//*")
    xpaths = [
        get_element_xpath(elem)
        for elem in elements
        if any(get_element_xpath(elem)[1:3])
    ]
    return xpaths

def save_to_csv(data, filename="../csv/02_xpaths.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["LocatorName", "LocatorValue", "LocatorType"])
        for row in data:
            writer.writerow([row[1], row[3], "XPath"])


def main():
    driver = webdriver.Chrome()
    try:
        driver.maximize_window()
        driver.get("http://51.20.64.81/#/employee")  # Replace with your target URL
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        time.sleep(3)  # Wait for the page to load completely

        xpaths = collect_xpaths(driver)
        save_to_csv(xpaths)
        print("XPaths saved to ../csv/02_xpaths.csv")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
