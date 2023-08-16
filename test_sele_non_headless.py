import undetected_chromedriver as uc 
# from seleniumwire import webdriver 
import pandas as pd
import time
import re
from random import randint
import glob
import pandas as pd
from pathlib import Path
import sys
from random import randint
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import DesiredCapabilities
import random
import re
from selenium_recaptcha_solver import RecaptchaSolver
from pyvirtualdisplay import Display
try:
    print("\nfile name is :" , sys.argv[0])
except:
    print('missing parameter')

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
number_of_groups = 3
proxy_group = int(sys.argv[1]) * 3
proxy_list = proxy_list[proxy_group:proxy_group+3]
proxy_list.append('localhost')

latest_proxy_index = proxy_list[0]

test_ua = 'Mozilla/5.0 (Windows NT 4.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36'
display = Display(visible=0, size=(800, 800))
display.start()

def set_up_driver(PROXY):
    global driver
    google = "https://google.com.vn"
    # replace 'your_absolute_path' with your chrome binary's aboslute path
    # driver = webdriver.Chrome(seleniumwire_options=options, options = chromeOptions)
    # driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', seleniumwire_options=options, options = chromeOptions)\
    try:
        options = Options()
        #options.add_argument("--headless=new")
        if PROXY != 'localhost':
            options.add_argument('--proxy-server=%s' % PROXY)
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f'--user-agent={test_ua}')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(options= options)
        driver.get(google)
        time.sleep(1)
    except Exception as e:
        driver.close()
        driver.quit()
        print(e)
        print('new network')
        options = Options()
        if PROXY != 'localhost':
            options.add_argument('--proxy-server=%s' % PROXY)
        #options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        options.add_argument(f'--user-agent={test_ua}')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-extensions")
        driver = webdriver.Chrome(options= options)
        driver.get(google)
        time.sleep(1)
    action = webdriver.ActionChains(driver )

    return driver, action


proxy_index = randint(0, len(proxy_list) - 1)
driver, action = set_up_driver(proxy_list[proxy_index])
reset_driver_number = 20
i = 0
def search_view(x):
    global driver
    global action
    global display
    global i
    global latest_proxy_index
    data = x['all']
    idx = x['id']
    text = data.lower()
    text = text.replace(' ', '+')
    text = text.replace(',', '+')
    text = text.replace('++', '+')
    google = "https://google.com.vn"
    url_contain = 'https://masothue.com'
    code = ''
    href = ''
    
    print(idx)
    # print(proxy_list[proxy_index])
    if(int(idx) % reset_driver_number == 0 and int(idx) >= reset_driver_number):
        driver.close()
        driver.quit()
        proxy_index = randint(0, len(proxy_list) - 1)
        while latest_proxy_index == proxy_index:
            proxy_index = randint(0, len(proxy_list) - 1)
        print("Proxy" ,proxy_list[proxy_index])
        latest_proxy_index = proxy_index
        driver, action = set_up_driver(proxy_list[proxy_index])
        print('ok')
    try:
        driver.get(google)
        time.sleep(1)
        print('Tìm kiếm')
        print(str(data) + " masothue.com")
        # print(driver.page_source)
        flaceholder = "Tìm"
        try:
            print('Tìm kiếm input')
            raw_html = str(driver.page_source)
            lang = re.search('Tìm', raw_html)
            box = re.search('textarea', raw_html)
            if not lang:
                print('change to english')
                flaceholder = "Search"
            if box:
                print('Change to text area')
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//textarea[contains(@title, "%s")]' % flaceholder)))
                search_form = driver.find_element(By.XPATH, '//textarea[contains(@title, "%s")]' % flaceholder)
            else:
                print('Search input')
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[contains(@title, "%s")]' % flaceholder)))
                search_form = driver.find_element(By.XPATH, '//input[contains(@title, "%s")]' % flaceholder)
            print('find box ok')
        except Exception as e:
            print('box fail')
        time.sleep(1)
        search_form.send_keys(str(data) + " masothue.com")
        # search_form.send_keys('test '+ str(i))
        time.sleep(1)
        action.send_keys(Keys.ENTER)
        action.perform()
    except Exception as e:
        print("Failedd ", e)
        return None
    time.sleep(1)
    list_a_masothue = driver.find_elements(By.XPATH, '//a[contains(@href, "%s")]' % url_contain)

    if not list_a_masothue:
        print('list href empty! maybe block by google')
        try:
            print('Try resolver capcha !')
            solver = RecaptchaSolver(driver=driver)
            recaptcha_iframe = driver.find_element(By.XPATH, '//iframe[@title="reCAPTCHA"]')
            solver.click_recaptcha_v2(iframe=recaptcha_iframe)
            time.sleep(5)
            print('Resolver capcha done !')
        except Exception as e:
            print("resolver capcha fail ", e)

    for a in list_a_masothue:
        href = a.get_attribute('href')
        print(href)
        match = re.search('(https://masothue.*)', str(href))
        if match:
            print(str(match.group(1)))
            return str(match.group(1))
        else:
            print('None')
            return None

path = '/home/ubuntu/data_all/data'
done_path = '/home/ubuntu/data_all/data_crawler'
file_group_number = int(sys.argv[1])

files = glob.glob(path + "/*.csv")
for filename in files:
    print(filename)
    file_number = Path(filename).stem
    try:
        file_number = int(file_number)
        if(file_number % number_of_groups == file_group_number):
            cols = ['name', 'location', 'note']
            df = pd.read_csv(filename , header = None, names = cols)
            df['id'] = df.index
            df['all'] = df.name.astype(str) +' ' + df.location.astype(str)
            df['code'] = df.apply(lambda x: search_view(x), axis= 1)
            done_df = df[['name', 'location', 'note','code']]
            done_path = done_path + 'done_' + str(file_number) + '.csv'
            print(done_df.id)
            done_df.to_csv(done_path)
    except:
        print('fail to get file chunk')
