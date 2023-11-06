from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

course_urls = []
course_data = {}

# Setup Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the page you want to scrape
url = 'https://thecourseforum.com/department/86/'

# Open the URL in a browser window
driver.get(url)

# Wait for the dynamic content to load
time.sleep(5)  # You can use explicit waits here with WebDriverWait instead of sleep

# Find all course links using the unique class name for links
elements = driver.find_elements(By.CLASS_NAME, "rating-card-link")

for element in elements:
    href = element.get_attribute('href')
    if href:
        course_urls.append(href)

# Close the browser window
#driver.quit()

course_urls_excel = pd.DataFrame(course_urls)
filename = "/Users/william/Desktop/Third-Year/ICE/CommunicationsPresentation/CourseForum/course_urls.xlsx"
course_urls_excel.to_excel(filename)
for course_url in course_urls:
    print(course_url)

print("FIRST PART DONE")

