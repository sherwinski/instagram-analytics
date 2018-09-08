from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import traceback
import sys
sys.path.insert(0, '../config/')
import auth

chrome_path = "/usr/local/Caskroom/chromedriver/2.41/chromedriver"
driver = webdriver.Chrome(chrome_path)

driver.get("https://www.instagram.com/")
driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a""").click()

time.sleep(1)
username_field = driver.find_element_by_xpath("""//*[@aria-label="Phone number, username, or email"]""")
username_field.send_keys(auth.username)
password_field = driver.find_element_by_xpath("""//*[@aria-label="Password"]""")
password_field.send_keys(auth.password)
password_field.send_keys(Keys.ENTER)

