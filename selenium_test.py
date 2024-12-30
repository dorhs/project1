from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
from webdriver_manager.chrome import ChromeDriverManager  
from logger import logging , url
import os
from selenium.common.exceptions import WebDriverException

# Configure headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver
try:
    driver = webdriver.Chrome(options=chrome_options)
except WebDriverException as e:
    logging.error(f"Failed to initialize WebDriver: {e}")
    exit(1)

# Start the script
try:
    try:
        logging.info('Register test Started')
        driver.get("http://localhost:8081/")
        logging.info('Entering the web page')
        logging.info('Page loaded')
    except WebDriverException as e:
        logging.error(f"Failed to load webpage: {e}")
        raise

    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
    except TimeoutException:
        logging.error("Timeout waiting for username field to load")
        raise

    try:
        input_element = driver.find_element(By.ID, "username")
        input_element.send_keys('qqqq')
        logging.info('Username was entered')
    except NoSuchElementException:
        logging.error("Username field not found")
        raise

    try:
        input_element = driver.find_element(By.ID, "password")
        input_element.send_keys('1111' + Keys.RETURN)
        logging.info('Providing password')
    except NoSuchElementException:
        logging.error("Password field not found")
        raise

    time.sleep(2)

    try:
        input_element = driver.find_element(By.ID, "Add Domain")
        input_element.send_keys(Keys.ENTER)
        logging.info('Entering Add domain page')
    except NoSuchElementException:
        logging.error("Add Domain button not found")
        raise

    time.sleep(2)

    try:
        input_element = driver.find_element(By.ID, "domain")
        input_element.send_keys('yahoo.com' + Keys.RETURN)
        logging.info('Adding domain')
    except NoSuchElementException:
        logging.error("Domain input field not found")
        raise

    time.sleep(2)

    try:
        home_link = driver.find_element(By.XPATH, '//a[@href="/dashboard"]')
        driver.execute_script("arguments[0].click();", home_link)
        logging.info('Entering Dashboard')
        logging.info('Back to dashboard')
    except NoSuchElementException:
        logging.error("Dashboard link not found")
        raise
    except WebDriverException as e:
        logging.error(f"Failed to click dashboard link: {e}")
        raise

    logging.info('Test Finished Successfully')
    time.sleep(3)

except Exception as e:
    logging.error(f"Test failed with error: {e}")
finally:
    driver.quit()
