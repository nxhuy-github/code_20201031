from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import  WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = "/home/nxhuy/Downloads/chromedriver_linux64/chromedriver"

driver = webdriver.Chrome(PATH)
driver.get("https://techwithtim.net")
print(driver.title)

# Access the element by the "name" attribute
# In this case, this is an input form
search = driver.find_element_by_name("s")
# Send the text we want to this input form
search.send_keys("test")
# Hit "Enter" to search
search.send_keys(Keys.RETURN)

# Get the entire source code HTML
# print(driver.page_source)

try:
    # This technique is called Explicit Wait in selenium
    # Try to wait (max 10s) until the element with "id=main" allocated in the screen
    # After we hit "Enter" like above, we need to wait to get the response
    main = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'main'))
    )
    #print(type(main))
    #print(main)
    articles = main.find_elements_by_tag_name("article")
    for article in articles:
        header = article.find_element_by_class_name("entry-summary")
        print(header.text)
finally:
    driver.quit()

#time.sleep(5)
#driver.quit()   
