from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from webdriver_manager.chrome import ChromeDriverManager  

# Configure headless Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up WebDriver
# Use ChromeDriverManager to automatically manage ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Start the script
try:
    driver.get("http://44.243.219.74:8081/")
    print('Entering the web page')

    WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.ID, 'username'))
    )

    input_element = driver.find_element(By.ID, "username")
    input_element.send_keys('qqqq')
    print('Username was entered')

    input_element = driver.find_element(By.ID, "password")
    input_element.send_keys('1111' + Keys.RETURN)
    print('Providing password')
    time.sleep(2)

    input_element = driver.find_element(By.ID, "Add Domain")
    input_element.send_keys(Keys.ENTER)
    print('Entering Add domain page')

    time.sleep(2)

    input_element = driver.find_element(By.ID, "domain")
    input_element.send_keys('yahoo.com' + Keys.RETURN)
    print('Adding domain')
    time.sleep(2)

    home_link = driver.find_element(By.XPATH, '//a[@href="/dashboard"]')
    driver.execute_script("arguments[0].click();", home_link)

    print('Entering Dashboard')
    print('Back to dashboard')
    print('Test Finished Successfully')
    time.sleep(3)

finally:
    driver.quit()
