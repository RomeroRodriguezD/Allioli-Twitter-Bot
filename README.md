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


