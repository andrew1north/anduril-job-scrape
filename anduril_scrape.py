from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, os, csv

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
        try:
            # Get the href attribute
            href = job_link.get_attribute('href')
        except Exception as e:
            href = "Not found"
            
        try:
            # Open the link in a new tab
            driver.execute_script("window.open(arguments[0]);", href)
            
            # Switch to the new tab
            driver.switch_to.window(driver.window_handles[-1])
            
            # Wait for the job description to load
            time.sleep(2)
            
            # Get job title
            try:
                job_title = driver.find_element(By.XPATH, '//*[@id="header"]/h1').text
            except Exception as e:
                job_title = "Not found"
            
            # Get company
            try:
                company = driver.find_element(By.CSS_SELECTOR, 'span.company-name').text
            except Exception as e:
                company = "Not found"
            
            # Get Location
            try:
                location = driver.find_element(By.CSS_SELECTOR, 'div.location').text
            except Exception as e:
                location = "Not found"
            
            # Get the content intro
            try:
                content_intro = driver.find_element(By.CSS_SELECTOR, 'div.content-intro').text
            except Exception as e:
                content_intro = "Not found"
            
            # Get all text from div with id "content"
            try:
                content_para = driver.find_element(By.ID, 'content')
                job_description = content_para.text
            except Exception as e:
                job_description = "Not found"

            # Get pay range
            try:
                pay_range = driver.find_element(By.CSS_SELECTOR, 'div.pay-range').text
            except Exception as e:
                pay_range = "Not found"
            
            # Write the extracted information to the CSV file
            writer.writerow([job_title, company, location, content_intro, job_description, pay_range])

            # Close the new tab
            driver.close()

            # Switch back to the original tab
            driver.switch_to.window(driver.window_handles[0])

            # Wait for the job listings to reload (adjust the wait time as necessary)
            time.sleep(3)
            
        except Exception as e:
            print(f"Failed to process job link: {href}")
            continue

# Close the WebDriver
driver.quit()