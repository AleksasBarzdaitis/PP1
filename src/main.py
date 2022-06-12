import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re
import html


url = 'https://www.aruodas.lt/namai/vilniuje/antakalnyje/'
op = webdriver.FirefoxOptions()
ffdriver = webdriver.Firefox(service=FFService('src/drivers/geckodriver_v0.31.0.exe'), options=op)

target_button = "button[id*='onetrust-accept-btn-handler']"

ffdriver.get(url)
wait = WebDriverWait(ffdriver, 15)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, target_button)))
cookies_button = ffdriver.find_element(By.CSS_SELECTOR, target_button)
cookies_button.click()

def get_data():
    rows = ffdriver.find_elements(By.CSS_SELECTOR, '*.list-row')
    data = []

    time.sleep(2)
    for row in rows:
        try:
            address = row.find_element(By.CSS_SELECTOR, 'td.list-adress > h3 > a')
            price = row.find_element(By.CSS_SELECTOR, 'td.list-adress > div > span.list-item-price')
            area = row.find_element(By.CSS_SELECTOR, 'td.list-AreaOverall')
        except NoSuchElementException:
            continue
        delim = "\\n"
        raw_text = "%r"%address.text
        split_raw = raw_text.split(delim)
        clean_address = ' '.join(split_raw)
        data.append({"Address":clean_address, "Price":price.text, "Area":area.text})
    for d in data:
        print(d)

while(True):
    next_page_button = ffdriver.find_element(By.LINK_TEXT, '»')
    get_data()
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((next_page_button)))
    href_data = next_page_button.get_attribute('href')
    if href_data is None:
        break
    else:
        next_page_button.click()

time.sleep(1)

# print(ffdriver.)
ffdriver.quit()