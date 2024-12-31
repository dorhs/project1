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
    time.sleep(2)
    try:
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
    except TimeoutException:
        logging.error("Timeout waiting for username field to load")
        raise
    time.sleep(2)
    try:
        input_element = driver.find_element(By.ID, "username")
        input_element.send_keys('baha')
        logging.info('Username was entered')
        print('test')
    except NoSuchElementException:
        logging.error("Username field not found")
        raise
    time.sleep(2)
    try:
        input_element = driver.find_element(By.ID, "password")
        input_element.send_keys('baha' + Keys.RETURN)
        logging.info('Providing password')
    except NoSuchElementException:
        logging.error("Password field not found")
        raise

    time.sleep(2)

    try:
        # נחכה שהסרגל הצדדי יטען
        sidebar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sidebar"))
        )
        
        # נגדיר גודל חלון ברור
        driver.set_window_size(1920, 1080)
        
        # נמצא את הקישור Add Domain
        add_domain_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a#Add\\ Domain'))
        )
        
        # ננסה לגלול אל האלמנט לפני הלחיצה
        driver.execute_script("arguments[0].scrollIntoView(true);", add_domain_link)
        
        # נוסיף המתנה קצרה אחרי הגלילה
        time.sleep(1)
        
        # ננסה ללחוץ באמצעות JavaScript
        driver.execute_script("arguments[0].click();", add_domain_link)
        
        logging.info('Successfully clicked Add Domain link')
        
        try:
            # נמתין לטעינת הדף החדש ולהופעת שדה הקלט
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "domain"))
            )
            
            # נמצא את שדה הקלט ונכניס את הדומיין
            input_element = driver.find_element(By.ID, "domain")
            input_element.clear()  # ננקה כל טקסט קיים
            input_element.send_keys('yahoo.com')
            
            # נחפש את כפתור השליחה ונלחץ עליו
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            
            logging.info('Domain submitted successfully')
            
            time.sleep(2)
        
        except TimeoutException as e:
            logging.error("Timeout waiting for Add Domain link")
            logging.error(f"Current URL: {driver.current_url}")
            logging.error(f"Page source: {driver.page_source}")
            raise
    except Exception as e:
        logging.error(f"Failed to click Add Domain link: {str(e)}")
        # נוסיף מידע נוסף לדיבוג
        logging.error(f"Element position: {add_domain_link.location if 'add_domain_link' in locals() else 'Unknown'}")
        logging.error(f"Window size: {driver.get_window_size()}")
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
