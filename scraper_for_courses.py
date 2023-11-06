from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
import pandas as pd
course_urls = []
course_data = {}

filename = "/Users/william/Desktop/Third-Year/ICE/CommunicationsPresentation/CourseForum/course_urls.xlsx"
course_urls_df = pd.read_excel(filename)
course_urls = course_urls_df["URLS"].tolist()

# Setup Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    for url in course_urls:
    # Go to the course URL
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Get the initial count of professors
        professor_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rating-card-link")))
        number_of_professors = len(professor_links)


        MAX_ITERATIONS = 10
        # Use index to iterate over professors

        visited_professors = 0
        for i in range(MAX_ITERATIONS):
            if visited_professors == number_of_professors:
                break
            # Fetch the list of professors again to avoid stale element reference
            professor_links = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".rating-card-link")))

            professor = professor_links[visited_professors]
            

            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView();", professor)
            #wait.until(EC.visibility_of(professor))  # Wait for the element to be visible

            if professor.is_displayed():
                try:
                    # Attempt to click the professor link using JavaScript
                    driver.execute_script("arguments[0].click();", professor)

                    # Adjust the selector to match the layout of the professor's page
                    gpa_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".gpa-text")))
                    gpa = gpa_element.text
                    print(gpa)
                    hours_per_week_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rating-card-num.hours-num")))
                    hours_per_week = hours_per_week_element.text
                    print(hours_per_week)
                    professor_name = url.strip("https://thecourseforum.com/course/") + str(visited_professors)

                    # Store the data in the dictionary
                    course_data[professor_name] = {
                        'GPA': gpa,
                        'Hours per Week': hours_per_week
                    }

                except ElementNotInteractableException:
                    print(f"Could not interact with the element for {professor_name}. It might be hidden.")
                finally:
                    # Navigate back to the course page
                    driver.back()
            else:
                print(f"Skipping {professor.text.strip()} as it is not visible on the screen.")


            # Increment the index for the next iteration
            visited_professors += 1
except Exception as e:
    print("An error occured")
finally:
    
    df_gpas_and_hours_studying = pd.DataFrame.from_dict(course_data, orient='index')
    filename = "/Users/william/Desktop/Third-Year/ICE/CommunicationsPresentation/CourseForum/data.xlsx"
    df_gpas_and_hours_studying.to_excel(filename)
    driver.quit()

# Print the collected data
for professor_name in course_data:
    print(professor_name, course_data[professor_name])
    # Close the browser once data collection is complete
    

# Convert the dictionary to a pandas DataFrame
# df_gpas_and_hours_studying = pd.DataFrame.from_dict(course_data, orient='index')
# filename = "/Users/william/Desktop/Third-Year/ICE/CommunicationsPresentation/CourseForum/data.xlsx"
# df_gpas_and_hours_studying.to_excel(filename)

# # Print the collected data
# for professor_name in course_data:
#     print(professor_name, course_data[professor_name])
