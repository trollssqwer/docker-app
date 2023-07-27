import undetected_chromedriver as uc 
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

try:
    print("\nfile name is :" , sys.argv[0])
    print("\ngroup number is :" , sys.argv[1])
except:
    print('missing parameter')

proxy_list =[
    'http://0806hqnbyo:onet.com.vn@103.59.170.209:13057',
    'http://0806hqnbyo:onet.com.vn@103.170.246.5:13057',
    'http://0806hqnbyo:onet.com.vn@103.170.246.23:13057',
    'http://0806hqnbyo:onet.com.vn@103.59.170.111:13057',
    'http://0806hqnbyo:onet.com.vn@103.59.170.110:13057',
    'http://0806hqnbyo:onet.com.vn@103.59.170.109:13057',
    'http://0806hqnbyo:onet.com.vn@103.59.170.108:13057',
    'http://0806hqnbyo:onet.com.vn@103.59.170.107:13057',
    'http://0806hqnbyo:onet.com.vn@103.59.170.106:13057',
    'http://0806hqnbyo:onet.com.vn@103.59.170.222:13057'
]

def set_up_driver(PROXY):
    chromeOptions = Options()
    chromeOptions.add_argument("--disable-extensions")
    chromeOptions.add_argument("--incognito")
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("start-maximized")
    chromeOptions.add_argument('--no-sandbox')
    # replace 'your_absolute_path' with your chrome binary's aboslute path
    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',options=chromeOptions)
    # driver = webdriver.Chrome(seleniumwire_options=options, options = chromeOptions)
    action = webdriver.ActionChains(driver)
    return driver, action

proxy_index = randint(0, len(proxy_list) - 1)
driver, action = set_up_driver(proxy_list[proxy_index])
reset_driver_number = 5
def search_view(x):
    global driver
    global action
    data = x['all']
    idx = x['id']
    text = data.lower()
    text = text.replace(' ', '+')
    text = text.replace(',', '+')
    text = text.replace('++', '+')
    google = "https://google.com"
    url_contain = 'https://masothue.com'
    code = ''
    href = ''
    driver.get(google)
    print(idx)
    if(int(idx) % reset_driver_number == 0 and int(idx) >= reset_driver_number):
        driver.close()
        driver.quit()
        proxy_index = randint(0, len(proxy_list) - 1)
        driver, action = set_up_driver(proxy_list[proxy_index])
        driver.get(google)
        print('ok')

    try:
        flaceholder = "Tìm kiếm"
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//textarea[contains(@title, "%s")]' % flaceholder)))
        search_form = driver.find_element(By.XPATH, '//textarea[contains(@title, "%s")]' % flaceholder)
        search_form.clear()
        search_form.send_keys(str(data) + " masothue.com")
        # time.sleep(1)
        action.send_keys(Keys.ENTER)
        action.perform()
    except Exception:
        print("Failed")
        return None
    list_a_masothue = driver.find_elements(By.XPATH, '//a[contains(@href, "%s")]' % url_contain)
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
path = '/app/data/'
done_path = '/app/data_done/'
file_group_number = sys.argv[1]
number_of_groups = 4
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
