from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import traceback
import math
import sys
sys.path.insert(0, '../config/')
import auth

liked_by = []
row_dict = {}

print("Working...")
chrome_path = "/usr/local/Caskroom/chromedriver/2.41/chromedriver"
driver = webdriver.Chrome(chrome_path)
# driver.maximize_window()
driver.set_window_position(0,0)
driver.set_window_size(1440,1440)
# driver.fullscreen_window()

# Navigate to website
driver.get("https://www.instagram.com/")
driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a""").click()

# Go through auth flow
time.sleep(1)
username_field = driver.find_element_by_xpath("""//*[@aria-label="Phone number, username, or email"]""")
username_field.send_keys(auth.username)
password_field = driver.find_element_by_xpath("""//*[@aria-label="Password"]""")
password_field.send_keys(auth.password)
submit_button = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button""")
submit_button.click()

# Navigate to user profile
time.sleep(2)
driver.get("https://www.instagram.com/nissanxinfiniti/")
time.sleep(1)

# Per given post, record all users that liked a given post 
# time.sleep(10)
# get number of posts
posts = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span""")
num_posts = int(posts.text)
print "num posts:", num_posts
posts_per_row = 3
posts_per_page = 8
total_rows = int(math.ceil(num_posts / float(posts_per_row)))
page_scrolls = num_posts / float(posts_per_page)
page_scrolls = int(math.ceil(page_scrolls))
total_posts_seen = 0

print "num rows:", total_rows
for index in range (1, (posts_per_page*page_scrolls), 1):
#for index in range (1, total_rows, 1):
	try:
		print "row number:",index

		#next_row = driver.find_elements(By.XPATH, """//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div["""+str(index)+"""]""")
		#if(not next_row):
		#	print "End of page"
		parent_div = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div""")
		# print "bottom padding: ", parent_div.get_attribute("[0].style.paddingBottom")
		# print "top padding: ", parent_div.get_attribute('padding-top')
		
		next_row = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div["""+str(index)+"""]""")

		for post in range(1,4):
				if(post == 1):
					key_post = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div["""+str(index)+"""]/div["""+str(post)+"""]/a""")
					#first_row.get()
					print 'href: ' , str(key_post.get_attribute('href'))[28:39]

					if(key_post not in row_dict):
						row_dict = {'key_post': key_post.get_attribute('href'), 'row_num': index, 'checked': False}
					print row_dict

				# -- look at each post --
				# next_post = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div["""+str(index)+"""]/div["""+str(post)+"""]""").click()
				# time.sleep(1.5)
				# driver.find_element_by_xpath("""/html/body/div[3]/div/button""").click()
				# time.sleep(.5)
				# total_posts_seen += 1
				# print "Looking at post number: ", total_posts_seen

		if(index > 1):
			print "searching dict"
			for sub_index in range (1,9):
				print "sub_index: ", sub_index
				search_row = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div[2]/article/div[1]/div/div["""+str(index)+"""]/div[1]/a""")
				search_row_href = str(search_row.get_attribute('href')[28:39])
				if(search_row_href not in row_dict):
					row_dict[len(row_dict)] = {'key_post':search_row_href, 'row_num': index, 'checked': False}
			print row_dict

		#driver.find_elements(By.XPATH,'/html/body/span/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]')
		#last_post = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/div[2]/article/div[2]""")
		#driver.execute_script("arguments[0].scrollIntoView();", last_post)
		#print "Total posts seen: ", total_posts_seen
		time.sleep(1)
	except Exception as e:
		raise e
	else:
		pass

print "End of page"
# first post
# driver.find_element_by_xpath("""/html/body/span/section/main/div/div[2]/article/div[1]/div/div[1]/div[1]""").click()
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