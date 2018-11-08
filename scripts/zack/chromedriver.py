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
    TargetUser = 'cooooooooooochieeee'
    chrome_path = path.driverPath
    driver = webdriver.Chrome(chrome_path)
    # driver.maximize_window()
    driver.set_window_position(0,0)
    driver.set_window_size(1440,1440)
    # driver.fullscreen_window()

    # Navigate to website
    driver.get("https://www.instagram.com/accounts/login")
    #driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a""").click()

    #display = Display(visible=0, size=(800, 600))
    #display.start()

    #browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver')
    print("Browser Initialized")

    time.sleep(1)
    #username_field = driver.find_element_by_xpath("""//*[@aria-label="Phone number, username, or email"]""")
    username_field = driver.find_element_by_name("username")
    username_field.send_keys(auth.username)
    password_field = driver.find_element_by_xpath("""//*[@aria-label="Password"]""")
    password_field.send_keys(auth.password)
    #submit_button = driver.find_element_by_xpath("""//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/button""")
    #submit_button.click()
    password_field.send_keys(Keys.ENTER)

    # Navigate to user profile
    time.sleep(2)
    driver.get("https://www.instagram.com/"+TargetUser+"/")
    time.sleep(1)

    browser = driver
    # browser.get('https://www.instagram.com/accounts/login/')

    # time.sleep(3)
    # UsernameBox = browser.find_element_by_name("username")
    # UsernameBox.send_keys(auth2.username)

    # PasswordBox = browser.find_element_by_xpath("//*[@aria-label='Password']")
    # PasswordBox.send_keys(auth2.password)
    # PasswordBox.send_keys(Keys.ENTER)

    # time.sleep(3)

    # browser.get("https://www.instagram.com/zackst/")

    # time.sleep(6)
    
    RowDict = {}
    ProcessCheck = {}
    likedBy = []
    rownum = 0
    LikeCount = {}


    class ProfCodes:
        row = ".Nnq7C"
        pic = ".v1Nh3"
        picOpen = ".v1Nh3 a"
        rowFull = "Nnq7C weEfm"
        followerList = ".jSC57 .PZuss"
        likeList = ".D7Y-g .PZuss"

    def GetFollowers():
        FollowersOpen = browser.find_element_by_css_selector("[href='/"+TargetUser+"/followers/']").click()
        time.sleep(2)

        LastUserName = "NoUser"
        OldLastUser = ""
        while LastUserName != OldLastUser:
            LastUser = browser.find_element_by_css_selector(ProfCodes.followerList + " li:last-child")
            if LastUserName != OldLastUser:
                print("New One")
            ScrollLast = browser.execute_script("document.querySelector('"+ProfCodes.followerList+" li:last-child').scrollIntoView()")
            #print(LastUser.text)
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

    def ScanLikes(num_likes):
        users_per_page = 12
        num_scrolls = num_likes / float(users_per_page)
        num_scrolls = int(math.ceil(num_scrolls))

        # makes all users who've liked the post visible via automatic scrolling
        for index in range (users_per_page, (users_per_page*num_scrolls), users_per_page):
            try:
                time.sleep(3)
                print("index:",index)
                last_user = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li["""+str(index)+"""]""")
                print("found user at li[",index,"]")
                driver.execute_script("arguments[0].scrollIntoView();", last_user)
            except Exception as e:
                raise
            else:
                pass

        time.sleep(1)

        actualLikes = len(browser.find_elements_by_css_selector(ProfCodes.likeList + " li"))
        print(num_likes," Likes Shown, ",actualLikes," Actually Available")
        # scans all users by name and stores in data struct
        for index in range(1 , actualLikes+1):
            print("index:", index)
            userName = driver.find_element_by_xpath("""/html/body/div[3]/div/div[2]/div/article/div[2]/div[2]/ul/div/li["""+str(index)+"""]/div/div[1]/div/div[1]/a""")
            print("adding user " + userName.text)
            if userName.text not in LikeCount:
                print(userName.text, "not here")
                LikeCount[userName.text] = 1
            else:
                print("other stuff happening")
                LikeCount[userName.text] += 1
            #RowDict.append((userName.text).encode("utf-8"))
            likedBy.append((userName.text).encode("utf-8"))

        print("Done adding users")

    def AssignRows(CurrentRows):
        print("Begin assigning rows...")
        for aRow in CurrentRows:
            FirstChild = aRow.find_elements_by_css_selector(ProfCodes.pic)[0]
            FirstChildID = FirstChild.find_element_by_css_selector("a").get_attribute("href")
            DirectID = FirstChildID.split("/")[4]
            if DirectID not in RowDict.values():
                RowDict["Row"+str(len(RowDict)+1)] = DirectID
                ProcessCheck[DirectID] = {'rowNum':len(RowDict) , 'checked':False}
                print("Row"+str(len(RowDict))+"("+DirectID+") added")
            else:
                print(DirectID + " Exists")

    def AllRows(CurrentRows):
        LastRow = CurrentRows[len(CurrentRows)-1]
        print("LastRow ",LastRow)
        LastRowChild = LastRow.find_elements_by_css_selector(ProfCodes.pic)[0]
        print("LastRowChild ",LastRowChild)
        LastRowID = LastRowChild.find_element_by_css_selector("a").get_attribute("href").split("/")[4]
        print("LastRowID ",LastRowID)
       
        while LastRowID not in RowDict.values():
        #print("LastRowID: " + LastRowID)
            # Add rows that have not yet been seen to dictionary
            AssignRows(CurrentRows)
            print("RowDict: ",RowDict)
        #print("Done assigning rows...")
            LastOldRow = CurrentRows[len(CurrentRows)-1]
            
            #LastOldRow.click()

            for iterator in CurrentRows:
                picNum = 0
                RowID = iterator.find_elements_by_css_selector(ProfCodes.pic)[0].find_element_by_css_selector("a").get_attribute("href").split("/")[4]
                if ProcessCheck[RowID]['checked'] == False:
                    for pic in iterator.find_elements_by_css_selector(ProfCodes.pic):
                        if not pic.find_elements_by_css_selector('[aria-label=Video]'):
                            pic.click()
                                #  print("Pic info: ", pic.find_element_by_css_selector("a").get_attribute("href").split("/")[4])
                            print("processing pic", picNum+1, " at row ",ProcessCheck[RowID]['rowNum'])
                            AccessLikeModal()
                            time.sleep(.75)
                            picNum += 1
                            ExitButton = driver.find_elements_by_xpath("""/html/body/div[3]/div/button""")
                            ExitButton[0].click()

                            if(picNum == 3):
                                ProcessCheck[RowID]['checked'] = True

            #ScanLikes()

            #exit out from individual post by clicking close botton

            #print(ExitButton)
            #if(not ExitButton.isEmpty()):
                
                
            
            time.sleep(3)
            NewRows = browser.find_elements_by_css_selector(ProfCodes.row)
            LastRow = NewRows[len(NewRows)-1]
            LastRowChild = LastRow.find_elements_by_css_selector(ProfCodes.pic)[0]
            LastRowID = LastRowChild.find_element_by_css_selector("a").get_attribute("href").split("/")[4]
            CurrentRows = NewRows


    Followers = GetFollowers()
    InitLikeCounter(Followers)

    CurrentRows = browser.find_elements_by_css_selector(ProfCodes.row)
    print("Rows: "+str(len(CurrentRows)))
    #print("Rows as []: ",CurrentRows)
    #AssignRows(CurrentRows)

    AllRows(CurrentRows)

    print(RowDict)
    print(LikeCount)

    #browser.save_screenshot('screenshot.png')

    browser.close()

except Exception as e:
    print(e)
    exc_type, exc_obj, exc_tb = sys.exc_info()
    print(exc_tb.tb_lineno)
    print("Encountered Error, closing browser")
    #browser.close()"""
