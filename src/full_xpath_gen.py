import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

load_dotenv()

def get_xpath(element):
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


def find_all_elements_with_xpath(driver, tag='*'):
    # Finds all elements of the specified tag within the <body>
    elements = driver.find_elements(By.XPATH, f"//body//{tag}")
    # Create a list of tuples containing each element's tag name and its XPath
    return [(element.tag_name, get_xpath(element)) for element in elements]


# Example usage
driver = webdriver.Chrome()  # Ensure you have the correct driver setup
driver.get(os.getenv('LINK'))  # Replace with the URL of your page

# Get all elements inside the body tag with their tag name and XPath
elements_with_xpaths = find_all_elements_with_xpath(driver)

# Print tag and XPath for each element
for tag, xpath in elements_with_xpaths:
    print(f"Tag: {tag}, XPath: {xpath}")

driver.quit()
