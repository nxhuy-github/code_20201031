from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "/home/nxhuy/Downloads/chromedriver_linux64/chromedriver"

driver = webdriver.Chrome(PATH)
driver.get("https://techwithtim.net")

# Get link on webpage
link = driver.find_element_by_link_text("Python Programming")
# Click on that link we just found
link.click()

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Beginner Python Tutorials'))
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'sow-button-19310003'))
    )
    element.click()

    # Get back to the previous page
    driver.back()

    # Go forward
    driver.forward()
except:
    driver.quit()