from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import traceback
import sys
sys.path.insert(0, '../config/')
import auth

liked_by = []
index = 1

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
time.sleep(2)
driver.get("https://www.instagram.com/nissanxinfiniti/")

# Per given post, record all users that liked a given post 
time.sleep(1)

# first post
driver.find_element_by_xpath("""/html/body/span/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]""").click()
time.sleep(2)

# button for modal showing likes
likes_expand = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/section[2]/div/a""")
likes_expand_text = likes_expand.text
post_length = int(likes_expand_text.split()[0])
	# print "post_length: " , post_length
likes_expand.click()

# first user to like
time.sleep(1)

	#like_modal = document.querySelector("body>div:nth-of-type(3)>div>div:nth-of-type(2)>div>div>div:nth-of-type(2)")
	#like_modal = driver.execute_script("""document.querySelector("body>div:nth-of-type(3)>div>div:nth-of-type(2)>div>article>div>div:nth-of-type(2)")""")
	#like_modal = driver.execute_script("document.querySelector('body>div:nth-of-type(3)>div>div:nth-of-type(2)>div>article>div>div:nth-of-type(2)')")

like_modal = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]""") #/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div
	#print "like_modal:", like_modal
print "modal height:", like_modal.get_attribute("scrollHeight")
like_modal_height = like_modal.get_attribute("scrollHeight")
while True:
	like_modal = like_modal.scroll(0,like_modal_height)	
	time.sleep(2)
	newHeight = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]""").get_attribute("scrollHeight")
	print "new height: ", newHeight
	if newHeight == like_modal_height:
		break
	like_modal_height = newHeight

time.sleep(1)
for index in range(1 , post_length):
	print "index:", index
	userName = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li["""+str(index)+"""]/div/div[1]/div/div[1]/a""")
	print "adding user " + userName.text
	liked_by.append((userName.text).encode("utf-8"))


print(liked_by)

print("Done")