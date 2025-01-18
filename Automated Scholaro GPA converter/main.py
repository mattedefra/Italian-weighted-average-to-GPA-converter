from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import pandas as pd
df = pd.read_csv('data/libretto.csv')
import time
WAIT_TIME = 0.2

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.scholaro.com/gpa-calculator/")
driver.maximize_window()
actions = ActionChains(driver)

#deny cookies
driver.find_element(By.CSS_SELECTOR, "#CybotCookiebotDialogBodyButtonDecline").click()

#select country
driver.find_element(by=By.CSS_SELECTOR, value='input.k-input-inner').send_keys('Italy')
time.sleep(WAIT_TIME)
actions.send_keys(Keys.ENTER).perform()

#add rows
driver.find_element(by=By.XPATH, value='//*[@id="gpaForm"]/div/div[1]/div[1]/div[5]/span[2]/span/input[1]').click()
time.sleep(WAIT_TIME)
actions.send_keys(Keys.BACKSPACE).perform()
time.sleep(WAIT_TIME)
actions.send_keys(f'{df.shape[0]-5}').perform()
driver.find_element(by=By.CSS_SELECTOR, value='button#addButton').click()
time.sleep(WAIT_TIME)

#finds text boxes for courses credits and grades
text_boxes = list(driver.find_elements(by=By.CSS_SELECTOR, value='tr td input'))

#fills boxes
ind=0
for t in text_boxes[1::3]:
    t.click()
    time.sleep(WAIT_TIME)
    actions.send_keys(f'{list(df.Credits)[ind]}').perform()
    ind+=1
    time.sleep(WAIT_TIME)
ind=0
for t in text_boxes[2::3]:
    t.click()
    time.sleep(WAIT_TIME)
    grade = list(df.Grades)[ind]
    if grade == 31: actions.send_keys(f'30L').perform()
    else: actions.send_keys(f'{grade}').perform()
    ind+=1
    time.sleep(WAIT_TIME)

#calculates gpa
driver.find_element(by=By.CSS_SELECTOR, value='button#calculateGPAButton').click()
time.sleep(WAIT_TIME)
gpa = driver.find_element(by=By.CSS_SELECTOR, value='span#cGPA').text
driver.quit()
print(f'GPA: {gpa}')