from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import traceback
import math
import sys
sys.path.insert(0, '../config/')
import auth

liked_by = []

print("Working...")
chrome_path = "/usr/local/Caskroom/chromedriver/2.41/chromedriver"
driver = webdriver.Chrome(chrome_path)
# driver.maximize_window()
driver.set_window_position(0,0)
driver.set_window_size(1440,1440)

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

#get number of posts
posts = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span""")
num_posts = int(posts.text)
print "num posts:", num_posts
posts_per_page = 8
page_scrolls = num_posts / float(posts_per_page)
page_scrolls = int(math.ceil(page_scrolls))

for index in range (posts_per_page, (posts_per_page*page_scrolls), 1):
	try:
		print "post index:",index
		#last_post = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div["""+str(index)+"""]""")
		last_post = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div[2]/article/div[2]""")
		print "found post at li[",index,"]"
		#driver.scroll_from_element(last_post, 0, 100)
		driver.execute_script("arguments[0].scrollIntoView();", last_post)
		time.sleep(1)
	except Exception as e:
		raise e
	else:
		pass

# first post
#driver.find_element_by_xpath("""/html/body/span/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]""").click()
time.sleep(2)

# button for modal showing likes
likes_expand = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/section[2]/div/a""")
likes_expand_text = likes_expand.text
num_likes = int(likes_expand_text.split()[0])
print "num_likes: " , num_likes
likes_expand.click()

# first user to like
time.sleep(2)
users_per_page = 12
num_scrolls = num_likes / float(users_per_page)
num_scrolls = int(math.ceil(num_scrolls))

print "num_scrolls:", num_scrolls

# scrolling to the bottom of the modal reveals the next 12 users who liked the post
# by scrolling ceiling(n/12) times, where n is the number of likes, we can reveal
# all n usernames 
for index in range (users_per_page, (users_per_page*num_scrolls), users_per_page):
	try:
		print "index:",index
		last_user = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li["""+str(index)+"""]""")
		print "found user at li[",index,"]"
		driver.execute_script("arguments[0].scrollIntoView();", last_user)
		time.sleep(2)
	except Exception as e:
		raise
	else:
		pass

# read and store each username found under the like modal
time.sleep(1)
for index in range(1 , num_likes+1):
	print "index:", index
	userName = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li["""+str(index)+"""]/div/div[1]/div/div[1]/a""")
	print "adding user " + userName.text
	liked_by.append((userName.text).encode("utf-8"))


print(liked_by)

print("Done")