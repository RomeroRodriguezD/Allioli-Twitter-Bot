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
  
    kill_cookies(driver) # Optional, just in case you don't quit the pop up
    # Get trending topics
    trends = check_trends(driver)
    # Make a Grok post based on one trend
    grok_post(driver, trends)
