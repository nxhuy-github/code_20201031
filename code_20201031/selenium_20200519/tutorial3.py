from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

PATH = "/home/nxhuy/Downloads/chromedriver_linux64/chromedriver"

driver = webdriver.Chrome(PATH)
driver.get("https://orteil.dashnet.org/cookieclicker/")

# Wait 5s
driver.implicitly_wait(5)

cookie = driver.find_element_by_id("bigCookie")
cookie_count = driver.find_element_by_id("cookies")

items = [driver.find_element_by_id("productPrice" + str(i)) for i in range(1, -1, -1)] 

actions = ActionChains(driver)
# Append this action to the queue (the chain)
actions.click(cookie)

for i in range(5000):
    # Actually perform the action(s) in the queue
    actions.perform()

    count = int(cookie_count.text.split(" ")[0])
    #print(count)

    for item in items:
        value = int(item.text)
        if value <= count:
            # To purchase item, we need to setup A NEW ACTION
            upgrade_actions = ActionChains(driver)
            # we need to move to the item on webpage
            upgrade_actions.move_to_element(item)
            # press the cursor down
            upgrade_actions.click()
            # do this action
            upgrade_actions.perform()
