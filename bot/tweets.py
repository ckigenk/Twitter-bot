from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import csv
from .constants import PATH, URL,SEARCH_TERM

class Tweet:
    def __init__(self):
        driver = webdriver.Chrome(service=Service(PATH))
        self.driver=driver
        self.driver.implicitly_wait(10)
        super(Tweet, self).__init__()

    def land_first_page(self):
        self.driver.get(URL)

    def login(self, username, password):
        username_el = self.driver.find_element(By.XPATH, '//input[@name="text"]')
        username_el.send_keys(username)
        username_el.send_keys(Keys.RETURN)
        password_el = self.driver.find_element(By.XPATH, '//input[@name="password"]')
        password_el.send_keys(password)
        password_el.send_keys(Keys.RETURN)
    
    def search(self, search_term):
        search_el=self.driver.find_element(By.XPATH, '//input[@aria-label="Search query"]')
        search_el.send_keys(search_term)
        search_el.send_keys(Keys.RETURN)
        self.driver.find_element(By.LINK_TEXT, 'Latest').click()

    def get_tweet_data(self, tweet):
        try:
            name = tweet.find_element(By.XPATH, './/span[@class="css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"]').text
        except:
            return
        try:
            username=tweet.find_element(By.XPATH, './/div[@dir="ltr"]/child::span').text
        except:
            return
        try:
            time=tweet.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
        except:
            return
        try:
            comment = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]').text
        except:
            return
        try:
            retweets = tweet.find_element(By.XPATH, './/div[contains(@data-testid,"retweet")]').text
        except:
            return
        try:
            likes = tweet.find_element(By.XPATH, './/div[contains(@data-testid,"like")]').text
        except:
            return
        return (name, username, time, comment, retweets, likes)
            

    def scroll_scrape_all_tweets(self):
        tweet_ids = set()
        all_data=[]
        self.all_data=all_data
        scroll_attempts=0
        scrolling=True
        while scrolling:
            last_position=self.driver.execute_script("return window.pageYOffset;")
            tweets = self.driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')
            for tweet in tweets[-15:]:
                data = self.get_tweet_data(tweet)
                if data:
                    if data not in tweet_ids:
                        tweet_ids.add("".join(data))
                        all_data.append(data)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            curr_position = self.driver.execute_script("return window.pageYOffset;")
            if curr_position==last_position:
                if scroll_attempts>=3:
                    scrolling=False
                    self.driver.close()
                else:
                    scroll_attempts+=1

    def save_data(self):
        with open(f"{SEARCH_TERM}_tweets.csv", 'w', newline='',encoding='utf-8') as f:
            writer=csv.writer(f)
            header=['name', 'username', 'time', 'comment', 'retweets','likes']
            writer.writerow(header)
            writer.writerows(self.all_data)

            print(f"Tweet Scrapping Completed Succesfully! The tweet data has been saved in {SEARCH_TERM}.csv")
