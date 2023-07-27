from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

CHROMEDRIVER_PATH = '/usr/local/bin/chromedriver'
service = Service
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
ser = Service(executable_path='/usr/local/bin/chromedriver')
driver = webdriver.Chrome(service=service)
driver.get("https://www.google.com")
print(driver.title)
driver.close()