from selenium import webdriver
from selenium.webdriver.common.by import By

# Set up the WebDriver (make sure the path to the WebDriver is correct)
driver = webdriver.Chrome()

# Load the webpage
url = 'http://github.com'  # Replace with your target URL
driver.get(url)

# Get the specific region element (example with body, can be any other region)
region = driver.find_element(By.TAG_NAME, 'body')

# Get all elements within the specific region
elements = region.find_elements(By.XPATH, './/*')

# Function to generate XPath in the form //tagname[@attribute='value']
def generate_xpath(element):
    tag = element.tag_name
    for attr in ['id', 'name', 'type', 'placeholder']:
        value = element.get_attribute(attr)
        if value:
            return f"//{tag}[@{attr}='{value}']"
    return f"//{tag}"  # Fallback to tag name if no preferred attribute is found

# Generate and print XPaths for all elements within the specific region
for element in elements:
    xpath = generate_xpath(element)
    print(xpath)

# Close the WebDriver
driver.quit()
