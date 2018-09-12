from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import traceback
import sys
sys.path.insert(0, '../config/')
import auth

liked_by = []
index = 0

print("Working...")
chrome_path = "/usr/local/Caskroom/chromedriver/2.41/chromedriver"
driver = webdriver.Chrome(chrome_path)

# Navigate to website
driver.get("https://www.instagram.com/")
driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a""").click()

# Go through auth flow
time.sleep(1)
username_field = driver.find_element_by_xpath("""//*[@aria-label="Phone number, username, or email"]""")
username_field.send_keys(auth.username)
password_field = driver.find_element_by_xpath("""//*[@aria-label="Password"]""")
password_field.send_keys(auth.password)
password_field.send_keys(Keys.ENTER)

# Navigate to user profile
time.sleep(1)
driver.get("https://www.instagram.com/nissanxinfiniti/")

# Per given post, record all users that liked a given post 
time.sleep(1)

# first post
driver.find_element_by_xpath("""/html/body/span/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]""").click()
time.sleep(1)

# button for modal showing likes
likes_expand_text = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/section[2]/div/a""").text
post_length = int(likes_expand_text.split()[0])
likes_expand.click()

# first user to like
time.sleep(1)
userName = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li[1]/div/div[1]/div/div[1]/a""")
liked_by.append(userName.text)


print(liked_by)

print("Done")