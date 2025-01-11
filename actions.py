from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import keyboard as kb
import random

USER = 'set_your_own_as_environment_variable'
PWD = 'set_your_own_as_environment_variable'
WEB = 'https://x.com/i/flow/login'

##### FUNCTIONALITIES #####

def get_driver():
    """Gets a webdriver that will perform every action"""
    driver = webdriver.Firefox()
    return driver

def kill_cookies(driver):
    """Accepts cookies. Optional for automated pipelines. """
    COOKIES = '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/button[1]'

    try:
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, COOKIES)))
        cookies = driver.find_element(By.XPATH, COOKIES)
        cookies.click()
        print('Cookies accepted.')

  def open_x(driver, user, passwd):
    """Performs automatic login, as long as it doesn't ask you email + username + pwd, which happens
        after many automated logins in a short period.
    """
    COOKIES = '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/button[1]'
    USER_XPATH = "//input[@autocomplete='username']"
    NEXT_BUTTON = "/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/button[2]"
    PWD_XPATH = "//input[@autocomplete='current-password']"
    LOGIN = "//button[@data-testid='LoginForm_Login_Button']"
    POST_XPATH = "//span[text()='Post']"

    # Open login page
    web = 'https://x.com/i/flow/login'
    driver.get(web)
    driver.maximize_window()

    # Accept cookies
    try:
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, COOKIES)))
        cookies = driver.find_element(By.XPATH, COOKIES)
        cookies.click()
        print('Cookies accepted.')
    except:
        print('No cookies popup detected.')

    time.sleep(0.5)

    # Set username
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, USER_XPATH)))
        username = driver.find_element(By.XPATH, USER_XPATH)
        username.send_keys(user)
        next_button = driver.find_element(By.XPATH, NEXT_BUTTON).click()
    except:
        raise Exception("Username field not found.")

    # Set password
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, PWD_XPATH)))
        pwd = driver.find_element(By.XPATH, PWD_XPATH)
        pwd.send_keys(passwd)
        login_button = driver.find_element(By.XPATH, LOGIN).click()
    except:
        raise Exception("Pwd field not found.")
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, POST_XPATH)))
        print('Account logged in!')
    except:
        raise Exception("Can't log in. Check possible credential errors.")

def check_trends(driver):
    """Checks trending topics. It can be set for "For you" based ones or general trends. """
    TRENDS_FORYOU = "https://x.com/explore/tabs/for-you"
    GENERAL_TRENDS = "https://x.com/explore/tabs/trending"

    TRENDS_XPATH = "//.[@data-testid='trend']"

    trends_list = []

    driver.get(TRENDS_FORYOU)

    # Get trending topics

    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, TRENDS_XPATH)))
        time.sleep(2)
        trends = driver.find_elements(By.XPATH, TRENDS_XPATH)
        for trend in trends:
            try:
                spans = trend.find_elements(By.TAG_NAME, 'span')
                if len(spans) > 1:  # Should be at least 2 elements per trend
                    second_span_text = spans[1].text.strip()  # Gets text from second span, which is the useful one
                    if ' ago' not in second_span_text and "posts" not in second_span_text: # Avoid news and other undesired stuff
                        trends_list.append(second_span_text)
            except Exception as e:
                print(f"Error processing trend: {e}")
    except Exception as e:
        print(f"Error loading trends: {e}")

    return trends_list

def grok_post(driver, trends):
    """Uses the captured trends list to pick a random one and ask Grok to create an image based on it.
       Then it uses the one that matches visual coordinates (xoffset + yoffset) and makes a post with
       "#trend".
    """
    GROK_URL = "https://x.com/compose/post/grok"
    TEXT_AREA = "//textarea[@placeholder]"
    TWEET_BUTTON = "//button[@data-testid='tweetButton']"
    POST_ACTION = "//a[@data-testid='SideNav_NewTweet_Button']"

    print('Trends: ', trends) # Check trends
    topic = random.choice(trends)
    topic_string = f"Make a photo of {topic}"
    tweet_string = f"#{topic}"
  
    driver.get(GROK_URL)

    # Ask for a photo
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, TEXT_AREA)))
        input_field = driver.find_element(By.XPATH, TEXT_AREA)
        input_field.send_keys(topic_string)
        input_field.send_keys(Keys.ENTER)
        print('Waiting 25 seconds for image generation...')
        time.sleep(25) #25 secs seems like a safe time lapse for Grok new image generation
    except:
        raise Exception("Can't find Grok input field.")

    # Choose photography by coordinates

    print('Clicking image')
    xoffset = 619
    yoffset = 290
    actions.move_by_offset(xoffset, yoffset).click().perform()
    time.sleep(0.5)
    post_but = driver.find_element(By.XPATH, POST_ACTION)
    actions.move_to_element(post_but).click().perform()
    print('Image clicked...')
    time.sleep(1)

    # Set the tweet text
    text_xpath = '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div[2]/div[1]/div/div/div/div[1]/div[2]/div/div/div/div/div/div/div/div/div/div/div[1]/div/div[1]/div/div/div/div/div/div[2]/div/div/div/div'    # Find text input and add trending topic with hashtag
    text_but = driver.find_element(By.XPATH, text_xpath)
    actions.move_to_element(text_but).click().perform()
    time.sleep(1)
    tweet_string = tweet_string.replace(' ', '')
    kb.write(f'{tweet_string} ', delay=0.1)
    time.sleep(1)

    post = driver.find_element(By.XPATH, TWEET_BUTTON)
    actions.move_to_element(post).click().perform()

    print('Post published!')
