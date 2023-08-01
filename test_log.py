from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

proxy_list =[
'103.170.247.122:10090',
'103.170.246.73:10090',
'103.170.246.106:10090',
'103.170.246.30:10090',
'103.170.246.137:10090',
'103.170.246.28:10090',
'103.170.247.97:10090',
'103.170.246.103:10090',
'103.170.246.51:10090',
'103.170.247.252:10090'
]

def set_up_driver(PROXY):
    chromeOptions = Options()
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument("--incognito")
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument("--allow-running-insecure-content")
    chromeOptions.add_argument("--ignore-certificate-errors")
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_argument('--proxy-server=%s' % PROXY)
    # replace 'your_absolute_path' with your chrome binary's aboslute path
    driver = webdriver.Chrome(seleniumwire_options=chromeOptions, options = chromeOptions)
    # driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', seleniumwire_options=options, options = chromeOptions)
    # driver = uc.Chrome(options= chromeOptions, driver_executable_path='/Users/tranthong/Downloads/chromedriver_mac64/chromedriver')
    action = webdriver.ActionChains(driver )
    return driver, action


while True:
    time.sleep(1)
    driver, action = set_up_driver(PROXY)
