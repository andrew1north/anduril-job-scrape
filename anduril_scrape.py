from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Set up the WebDriver (ensure you have the appropriate driver for your browser)
driver_path = 'path_to_your_chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)

# URL to crawl
url = "https://www.anduril.com/open-roles/?location=Costa+Mesa%2C+California%2C+United+States&department="

# Open the page
driver.get(url)

# Wait for the job listings to load (adjust the wait time as necessary)
time.sleep(5)

# Find all job links
job_links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/open-roles/"]')

# Create a directory to save job descriptions
output_dir = 'job_descriptions'
os.makedirs(output_dir, exist_ok=True)

# Loop through each job link and save the job description
for job_link in job_links:
    job_title = job_link.text
    job_link.click()
    
    # Wait for the job description to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.job-description')))
    
    # Get the job description
    job_description = driver.find_element(By.CSS_SELECTOR, '.job-description').text
    
    # Save the job description to a file
    file_name = f"{output_dir}/{job_title.replace('/', '_')}.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(job_description)
    
    
    # Go back to the main page
    driver.back() 
    
    # Wait for the job listings to reload (adjust the wait time as necessary)
    time.sleep(5)

# Close the WebDriver
driver.quit()