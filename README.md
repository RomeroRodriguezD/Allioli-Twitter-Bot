## Alliolli Twitter Bot ##
![image](https://github.com/user-attachments/assets/595841c3-96dc-4b0b-83fe-7fd87a8792a8)

A Selenium based Twitter bot to perform different actions. Still in a very early stage.

--------------------------------------------
### How to craft a simple pipeline ###

#### Step 1: Call a driver, action chain object and choose a login method: Either manual or automatic through the open_x() function ####

-For manual method use the keyboard module, so once you are done with the login, an F2 press will trigger the automated actions. 

-Otherwise, just call open_x(driver,username,password) and let it be:


```
# pipeline.py

from actions import get_driver, kill_cookies, check_trends, grok_post
from selenium.webdriver.common.action_chains import ActionChains

USER = 'set_your_own_as_environment_variable'
PWD = 'set_your_own_as_environment_variable'
WEB = 'https://x.com/i/flow/login'

if __name__ == "__main__":
    # Get a driver and action chains
    driver = get_driver()
    actions = ActionChains(driver)
    # Navigate to the login page
    driver.get(WEB)
    driver.maximize_window()
    # Perform manual login or uncomment open_x() and remove the wait for F2 press.
    # open_x(driver, USER, PWD)
    print('Press F2 once you are logged in')
    kb.wait('f2')

    # Add next actions below.
```

#### Step 2: Add desired actions that makes sense given the pipeline you are thinking about ####

In the example I've set, it will pick a random trending topic from the section "For you", ask Grok AI to make a photography about it, and use one of them to make a post with
the same hashtag.

```
# pipeline.py

from actions import get_driver, kill_cookies, check_trends, grok_post
from selenium.webdriver.common.action_chains import ActionChains

USER = 'set_your_own_as_environment_variable'
PWD = 'set_your_own_as_environment_variable'
WEB = 'https://x.com/i/flow/login'

if __name__ == "__main__":
    # Get a driver and action chains
    driver = get_driver()
    actions = ActionChains(driver)
    # Navigate to the login page
    driver.get(WEB)
    driver.maximize_window()
    # Perform manual login or uncomment open_x() and remove the wait for F2 press.
    # open_x(driver, USER, PWD)
    print('Press F2 once you are logged in')
    kb.wait('f2')

    # Add next actions below.

    kill_cookies(driver) # Optional, just in case you don't quit the pop up manually or if you just don't care
    # Get trending topics
    trends = check_trends(driver)
    # Make a Grok post based on one trend
    grok_post(driver, trends)

```

#### Step 3: Run and get the result ####

In this case, a random Grok photo about "Lavapiés", a place in Madrid that was temporally a trend.

![image](https://github.com/user-attachments/assets/df4b1fac-1401-4eff-bff7-5a1b2862eda9)

------------------------------------------------------------

### Current actions ###

- Login.

```def open_x(driver, user, passwd):
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
```

- Kill Cookies.

```
def kill_cookies(driver):
    """Accepts cookies. Optional. """
    COOKIES = '/html/body/div[1]/div/div/div[1]/div/div/div/div/div/div[2]/button[1]'

    try:
        WebDriverWait(driver, 6).until(EC.visibility_of_element_located((By.XPATH, COOKIES)))
        cookies = driver.find_element(By.XPATH, COOKIES)
        cookies.click()
        print('Cookies accepted.')
    except:
        print('No cookies popup detected.')
```

- Check and return trends.

```
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
        time.sleep(2) # Give some time for random ocasional delay loading
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
```

- Make a new Tweet with a photography made by Grok, using the same trend as hashtag.

```
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
```
