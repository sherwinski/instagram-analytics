from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.action_chains import ActionChains
import time
import traceback
import math
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
num_likes = int(likes_expand_text.split()[0])
print "num_likes: " , num_likes
likes_expand.click()

# first user to like
time.sleep(2)
num_scrolls = num_likes / float(12)
users_per_page = 12
num_scrolls = int(math.ceil(num_scrolls))

print "num_scrolls:", num_scrolls
	#actions = ActionChains(driver)

for index in range (users_per_page, (users_per_page*num_scrolls), users_per_page):
	try:
		print "index:",index
		last_user = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li["""+str(index)+"""]""")
		#last_user.location_once_scrolled_into_view()
		print "found user at li[",index,"]"
		driver.execute_script("arguments[0].scrollIntoView();", last_user)
		time.sleep(2)
	except Exception as e:
		raise
	else:
		pass

print "we've made it this far"
	# like_modal = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]""") #/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div
	# print "modal height:", like_modal.get_attribute("scrollHeight")

	# like_modal_height = like_modal.get_attribute("scrollHeight")
	# while True:
	# 	#like_modal = like_modal.scroll(0,like_modal_height)	
	# 	time.sleep(2)
	# 	newHeight = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]""").get_attribute("scrollHeight")
	# 	print "new height: ", newHeight
	# 	if newHeight == like_modal_height:
	# 		break
	# 	like_modal_height = newHeight


time.sleep(1)
for index in range(1 , num_likes+1):
	print "index:", index
	userName = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li["""+str(index)+"""]/div/div[1]/div/div[1]/a""")
	print "adding user " + userName.text
	liked_by.append((userName.text).encode("utf-8"))


print(liked_by)

print("Done")