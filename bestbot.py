from selenium import webdriver
from time import sleep
from random import randint
from configs import *
from datetime import datetime

class InstagramBot:
    def __init__(self, username, password, login_link, sleep_time_from, sleep_time_to):
        self.username = username
        self.password = password
        self.login_link = login_link
        self.sleep_time_from = sleep_time_from
        self.sleep_time_to = sleep_time_to

    # Login to Instagram
    def Login (self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome("V1\drivers\chromedriver", chrome_options=chrome_options)
        self.driver.get(login_link)
        sleep(4)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(6)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)

    # Follow people
    def Follow (self):
        ToFollowList = open("ToFollowList.txt", "r")
        Log = open("log.txt","a")

        for FollowName in ToFollowList:
            # Slepping till another Unfollow request
            random = randint(sleep_time_from, sleep_time_to)
            sleep(random)

            # Open profile
            self.driver.get("https://www.instagram.com/" + FollowName + "/")

            # Setting the current time
            now = datetime.now()
            time = now.strftime("%H:%M:%S")

            # Trying to follow person
            try:
                self.driver.find_element_by_xpath("//h2[contains(text(), 'This Account is Private')]")
                self.driver.find_element_by_css_selector(".y3zKF").click()
                Log.write("[" + time + "] SUCCESS: Waited " + str(random) + " sec. Followed private account: " + FollowName)
            except:
                try:
                    self.driver.find_element_by_xpath("//button[contains(text(), 'Follow')]").click()
                    Log.write("[" + time + "] SUCCESS: Waited " + str(random) + " sec. Followed public account: " + FollowName)
                except:
                    try:
                        self.driver.find_element_by_xpath("//button[contains(text(), 'Cancel')]").click()
                        Log.write("[" + time + "] WARNING: Waited " + str(random) + " sec. Already following: " + FollowName)
                    except:
                        Log.write("[" + time + "] WARNING: Waited " + str(random) + " sec. Already requested: " + FollowName)

    # Unfollow people
    def Unfollow (self):

        # Open files
        ToUnfollowList = open("ToUnfollowList.txt", "r")
        Log = open("log.txt","a")

        # Starting the loop
        for UnfollowName in ToUnfollowList:

            # Slepping till another Unfollow request
            random = randint(sleep_time_from, sleep_time_to)
            sleep(random)

            # Open profile
            self.driver.get("https://www.instagram.com/" + UnfollowName + "/")

            # Setting the current time
            now = datetime.now()
            time = now.strftime("%H:%M:%S")

            # Trying to unfollow person
            try:
                self.driver.find_element_by_xpath("//button[contains(text(), 'Following')]").click()
                self.driver.find_element_by_xpath("//button[contains(text(), 'Unfollow')]").click()
                Log.write("[" + time + "] SUCCESS: Waited " + str(random) + " sec. Unfollowed: " + UnfollowName)
            except:
                Log.write("[" + time + "] ERROR: Waited " + str(random) + " sec. Wasn't following or doesn't exist: " + UnfollowName)

    # Get follow list
    def GetFollowingList (self):

        # Open profile
        self.driver.get("https://www.instagram.com/" + username + "/")
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        sleep(2)

        #Scroll to the bottom
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = self.driver.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']

        # Print all the list into the file
        ToUnfollowList = open('ToUnfollowList.txt','w')
        for element in names:
            ToUnfollowList.write(element)
            ToUnfollowList.write('\n')
        ToUnfollowList.close()

bot = InstagramBot(username, password, login_link, sleep_time_from, sleep_time_to)
bot.Login()
bot.Follow()