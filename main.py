from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

PROMISED_UP = 15
PROMISED_DOWN = 500

# Notice: program will not run unless you input a valid twitter email/password below
TWITTER_EMAIL = "YOURTWITTEREMAIL@EMAIL.COM"
TWITTER_PASS = "YOURTWITTERPASSWORD"
chrome_driver_path = "C:\Development\chromedriver.exe"


class InternetSpeedTwitterBot():
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path)
        self.up = 0
        self.down = 0

    # Tests the internet speed, may take up to 1m
    def get_internet_speed(self):
        self.driver.get("https://speedtest.net")
        start_btn = self.driver.find_element_by_xpath(
            '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[1]/a')
        start_btn.click()
        time.sleep(50)
        close_btn = self.driver.find_element_by_xpath(
            '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[8]/div/div/div[2]/a')
        close_btn.click()
        self.down = self.driver.find_element_by_xpath(
            '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
        self.up = self.driver.find_element_by_xpath(
            '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[3]/div/div[2]/span').text

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/login")
        time.sleep(5)
        twitter_email = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')
        twitter_email.send_keys(TWITTER_EMAIL)
        twitter_password = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')
        twitter_password.send_keys(TWITTER_PASS)
        time.sleep(5)
        twitter_password.send_keys(Keys.ENTER)
        time.sleep(3)

        # Complaint template, not aimed at a specific internet provider here, strictly academic purposes
        complaint_template = f"Hey Internet Provider, why is my internet speed {speed_checker.down}down / {speed_checker.up}up when I pay for {PROMISED_DOWN}down/{PROMISED_UP}up?"
        tweet_compose = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/div[2]/div/div/div/div')
        tweet_compose.send_keys(complaint_template)
        time.sleep(5)
        tweet_send = self.driver.find_element_by_xpath(
            '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]/div/div[2]/div[1]/div/div/div/div[2]/div[4]/div/div/div[2]/div[3]')
        tweet_send.click()
        time.sleep(3)
        self.driver.quit()


speed_checker = InternetSpeedTwitterBot()
speed_checker.get_internet_speed()

print(f"Download: {speed_checker.down}")
print(f"Upload: {speed_checker.up}")

# If the upload/download speeds are less than what was promised by internet provider, tweets at them

if float(speed_checker.down) < PROMISED_DOWN or float(speed_checker.up) < PROMISED_UP:
    speed_checker.tweet_at_provider()
