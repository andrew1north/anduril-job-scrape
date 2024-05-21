from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Set up the WebDriver (ensure you have the appropriate driver for your browser)
driver_path = '/Users/andrewsmyth/Documents/chromedriver-mac-arm64/chromedriver'
service = Service(driver_path)
driver = webdriver.Chrome(service=service)

# URL to crawl
url = "https://www.anduril.com/open-roles/?location=Costa+Mesa%2C+California%2C+United+States&department="

# Open the page
driver.get(url)

# Wait for the job listings to load (adjust the wait time as necessary)
time.sleep(5)

# Find all job links
job_links = driver.find_elements(By.CSS_SELECTOR, 'a.JobListing_jobApplyBtn__KGnsS')

# Create a directory to save job descriptions
output_dir = 'job_descriptions'
os.makedirs(output_dir, exist_ok=True)

csv_file_path = os.path.join(output_dir, 'job_descriptions.csv')

with open(csv_file_path, mode='w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company', 'Location', 'Content Intro', 'Job Description', 'Pay Range'])

    for job_link in job_links:
        # Get the href attribute
        href = job_link.get_attribute('href')
        
        # Open the link in a new tab
        driver.execute_script("window.open(arguments[0]);", href)
        
        # Switch to the new tab
        driver.switch_to.window(driver.window_handles[-1])
        
        # Wait for the job description to load
        time.sleep(3)
        
        # Get job title
        job_title = driver.find_element(By.XPATH, '//*[@id="header"]/h1').text

        # Get company
        company = driver.find_element(By.CSS_SELECTOR, 'span.company-name').text

        # Get Location
        location = driver.find_element(By.CSS_SELECTOR, 'div.location').text

        # Get the content intro
        content_intro = driver.find_element(By.CSS_SELECTOR, 'div.content-intro').text

        # get the job description
        content_para = driver.find_element(By.ID, 'content')
        job_description = content_para.text

        # get pay range
        pay_range = driver.find_element(By.CSS_SELECTOR, 'div.pay-range').text
        
        
        # Print the extracted information
        print(f"Job Title: {job_title}")
        print(f"Company: {company}")
        print(f"Location: {location}")
        print(f"Content Intro: {content_intro}")
        print(f"Job Description: {job_description}")
        print(f"Pay Range: {pay_range}")
        print('-' * 40)

        # Close the new tab
        driver.close()

        # switch back to the original tab
        driver.switch_to.window(driver.window_handles[0])

        # Wait for the job listings to reload (adjust the wait time as necessary)
        time.sleep(3)

# Close the WebDriver
driver.quit()