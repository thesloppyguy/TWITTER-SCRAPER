from logging import lastResort
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from os import path
import csv
from time import sleep

# FUNCTIONS


def waiting_func(by_variable, attribute):
    try:
        WebDriverWait(driver, 20).until(
            lambda x: x.find_element(by=by_variable,  value=attribute))
    except (NoSuchElementException, TimeoutException):
        print('{} {} not found'.format(by_variable, attribute))
        exit()


def getdata(card):
    username = card.find_element_by_xpath(".//span").text
    tag = card.find_element_by_xpath('.//span[contains(text(), "@")]').text
    try:
        time = card.find_element_by_xpath(".//time").get_attribute('datetime')
    except NoSuchElementException:
        return
    tweet = card.find_element_by_xpath(
        ".//div[2]/div[2]/div[1]").text + card.find_element_by_xpath(".//div[2]/div[2]/div[1]").text
    comment = card.find_element_by_xpath('.//div[@data-testid="reply"]').text
    like = card.find_element_by_xpath('.//div[@data-testid="like"]').text
    retweet = card.find_element_by_xpath('.//div[@data-testid="retweet"]').text

    return (username, tag, time, tweet, comment, like, retweet)


cur_dir = path.dirname(__file__)
Chrome_driver = path.join(cur_dir, "bin\chromedriver.exe")

driver = webdriver.Chrome(executable_path=Chrome_driver)
x = input()
print(x)

driver.get(f"https://twitter.com/search?q={x}&src=typed_query&f=live")
sleep(5)
cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')


tweet_data_list = []
tweet_ids = set()
last_pos = driver.execute_script("return window.pageYOffset;")
scrolling = True

while scrolling:
    sleep(5)
    cards = driver.find_elements_by_xpath('//div[@data-testid="tweet"]')
    for i in cards:
        tweet = getdata(i)
        if tweet:
            tweet_id = "".join(tweet)
            if tweet_id not in tweet_ids:
                tweet_ids.add(tweet_id)
                tweet_data_list.append(tweet)
    scroll_try = 0
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        sleep(5)
        cur_pos = driver.execute_script("return window.pageYOffset;")
        if cur_pos == last_pos:
            scroll_try += 1
            if scroll_try >= 5:
                scrolling = False
                break
            else:
                sleep(2)
        elif len(tweet_data_list) >= 14500:
            scrolling = False
            break
        else:
            last_pos = cur_pos
            break

x = x.replace(" ", "_")
doc_dir = cur_dir+f"\docs\list_of_{x}_tweets.csv"
with open(doc_dir, 'w', newline='', encoding='utf-8') as f:
    header = ['username', 'tag', 'time', 'tweet', 'comment', 'like', 'retweet']
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(tweet_data_list)

driver.close()
