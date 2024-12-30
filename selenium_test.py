from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import logging
import time

# Configure headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver
try:
    driver = webdriver.Chrome(options=chrome_options)
    logging.info("WebDriver initialized successfully")
except WebDriverException as e:
    logging.error(f"Failed to initialize WebDriver: {e}")
    exit(1)

# Start the script
try:
    logging.info('Register test Started')
    driver.get("http://localhost:8081/")
    logging.info('Web page loaded')

    # Wait for username field
    username_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    username_field.send_keys("qqqq")
    logging.info("Username entered")

    # Wait for password field
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_field.send_keys("1111" + Keys.RETURN)
    logging.info("Password entered")

    # Wait for Add Domain button
    add_domain_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Add Domain"))  # Ensure ID matches HTML
    )
    add_domain_button.click()
    logging.info("Navigated to Add Domain page")

    # Add a domain
    domain_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "domain"))
    )
    domain_field.send_keys("yahoo.com" + Keys.RETURN)
    logging.info("Domain added")

    # Navigate back to Dashboard
    dashboard_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@href="/dashboard"]'))
    )
    driver.execute_script("arguments[0].click();", dashboard_link)
    logging.info("Navigated back to Dashboard")

    logging.info("Test Finished Successfully")

except NoSuchElementException as e:
    logging.error(f"Element not found: {e}")
    driver.save_screenshot("debug_screenshot.png")
    with open("debug_page_source.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
except TimeoutException as e:
    logging.error(f"Timeout occurred: {e}")
except WebDriverException as e:
    logging.error(f"WebDriver error: {e}")
finally:
    driver.quit()
