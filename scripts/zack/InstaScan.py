# -*- coding: utf-8 -*-
#from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import traceback
import math
from datetime import datetime
import sys
sys.path.insert(0, '../../config')
import auth
import path
# import auth2

try:
#if 1==1:
    TargetUser = 'zackst'
    chrome_path = path.driverPath
    driver = webdriver.Chrome(chrome_path)
    # driver.maximize_window()
    driver.set_window_position(0,0)
    driver.set_window_size(1440,1440)
    # driver.fullscreen_window()

    # Navigate to website
    driver.get("https://www.instagram.com/accounts/login")

    #display = Display(visible=0, size=(800, 600))
    #display.start()
    print("Browser Initialized")

    time.sleep(1)
    username_field = driver.find_element_by_name("username")
    username_field.send_keys(auth.username)
    password_field = driver.find_element_by_xpath("""//*[@aria-label="Password"]""")
    password_field.send_keys(auth.password)
    password_field.send_keys(Keys.ENTER)

    # Navigate to user profile
    time.sleep(2)
    driver.get("https://www.instagram.com/"+TargetUser+"/")
    time.sleep(1)

    browser = driver
    
    RowDict = {}
    ProcessCheck = {}
    likedBy = []
    rownum = 0
    LikeCount = {}

    #Define CSS codes for Selenium usage
    class ProfCodes:
        row = ".Nnq7C"
        pic = ".v1Nh3"
        picOpen = ".v1Nh3 a"
        rowFull = "Nnq7C weEfm"
        followerList = ".jSC57 .PZuss"
        likeList = ".D7Y-g .PZuss"

    #Function to procure followers of a profile 
    def GetFollowers():
        FollowersOpen = browser.find_element_by_css_selector("[href='/"+TargetUser+"/followers/']").click()
        time.sleep(2)

        LastUserName = "NoUser"
        OldLastUser = ""
        while LastUserName != OldLastUser:
            LastUser = browser.find_element_by_css_selector(ProfCodes.followerList + " li:last-child")
            if LastUserName != OldLastUser:
                print("More To Scroll")
            ScrollLast = browser.execute_script("document.querySelector('"+ProfCodes.followerList+" li:last-child').scrollIntoView()")
            time.sleep(2)
            OldLastUser = LastUserName
            LastUserName = browser.find_element_by_css_selector(ProfCodes.followerList + " li:last-child div div div div a").text
            print(OldLastUser + " " + LastUserName)

        YourFollowers = []
        for Follower in browser.find_elements_by_css_selector(ProfCodes.followerList + " li"):
            FollowerName = Follower.find_element_by_css_selector(".d7ByH a").text #xpath(".//div/div/div[1]/div/a").text
            YourFollowers.append(FollowerName)

        print(str(len(YourFollowers))+" followers found")
        ExitButton = browser.find_element_by_css_selector('[aria-label=Close]')
        ExitButton.click()
        return YourFollowers

    #Function to establish user dictionary and allow for checking of unengaged followers
    def InitLikeCounter(Followers):
        
        for Follower in Followers:
            LikeCount[Follower] = 0

    def AccessLikeModal():
       time.sleep(3)
       likes_expand_text = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/section[2]/div/button/span""")
       likes_expand_text = likes_expand_text.text
       num_likes = int(likes_expand_text.split()[0])
       print("num_likes: " , num_likes)
       likes_expand = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/section[2]/div/button""")
       likes_expand.click() 
       ScanLikes(num_likes)

    #Scan likes of each photo and add to dictionary
    def ScanLikes(num_likes):
        users_per_page = 12
        num_scrolls = num_likes / float(users_per_page)
        num_scrolls = int(math.ceil(num_scrolls))

        # makes all users who've liked the post visible via automatic scrolling
        LastUserName = "NoUser"
        OldLastUser = ""
        while LastUserName != OldLastUser:
            time.sleep(1.2)
            LastUser = browser.find_element_by_css_selector(ProfCodes.likeList + " li:last-child")
            if LastUserName != OldLastUser:
                print("More To Scroll")
            ScrollLast = browser.execute_script("document.querySelector('"+ProfCodes.likeList+" li:last-child').scrollIntoView()")
            #print(LastUser.text)
            time.sleep(2)
            OldLastUser = LastUserName
            LastUserName = browser.find_element_by_css_selector(ProfCodes.likeList + " li:last-child div div div div a").text
            print(OldLastUser + " " + LastUserName)

        time.sleep(1)

        actualLikes = len(browser.find_elements_by_css_selector(ProfCodes.likeList + " li"))
        print(num_likes," Likes Shown, ",actualLikes," Actually Available")
        # scans all users by name and stores in data struct
        for index in range(1 , actualLikes+1):
            print("index:", index)
            userName = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li["""+str(index)+"""]/div/div[1]/div/div[1]/a""")
            if userName.text not in LikeCount:
                print("Adding ",userName.text," to dictionary")
                LikeCount[userName.text] = 1
            else:
                print("Adding like from ",userName.text)
                LikeCount[userName.text] += 1
            #RowDict.append((userName.text).encode("utf-8"))
            likedBy.append((userName.text).encode("utf-8"))

        print("Done adding users")

    
    def AltCycle(CurrentPicture):
        CurrentPicture.click()
        time.sleep(1)
        #Need to add new different check for video. If function would just affect accesslikemodal
        AccessLikeModal()
        if browser.find_elements_by_css_selector(".coreSpriteRightPaginationArrow"):
            NextPicture = browser.find_element_by_css_selector(".coreSpriteRightPaginationArrow")
            AltCycle(NextPicture)
        


    Followers = GetFollowers()
    InitLikeCounter(Followers)

    FirstPicture = browser.find_elements_by_css_selector(ProfCodes.row)[0].find_elements_by_css_selector(ProfCodes.pic)[0]
    AltCycle(FirstPicture)

    #Need to add sorting function to provide their user's like count in a digestible format
    print(LikeCount)


    browser.close()

except Exception as e:
    print(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(exc_tb.tb_lineno)
    print("Encountered Error, closing browser")
    browser.close()