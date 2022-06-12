import time

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



url = 'https://www.aruodas.lt/namai/vilniuje/antakalnyje/'
target_button = "button[id*='onetrust-accept-btn-handler']"
op = webdriver.FirefoxOptions()
ffdriver = webdriver.Firefox(service=FFService('src/drivers/geckodriver_v0.31.0.exe'), options=op)

ffdriver.get(url)
wait = WebDriverWait(ffdriver, 15)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, target_button)))
cookies_button = ffdriver.find_element(By.CSS_SELECTOR, target_button)
cookies_button.click()
price = 'tr:nth-child(4) > td.list-adress > div > span.list-item-price'


while(True):
    next_page_button = ffdriver.find_element(By.LINK_TEXT, '»')
    test_price = ffdriver.find_element(By.CSS_SELECTOR, price)
    print(test_price.text)
    time.sleep(1)
    wait.until(EC.element_to_be_clickable((next_page_button)))
    href_data = next_page_button.get_attribute('href')
    if href_data is None:
        break
    else:
        next_page_button.click()

    # wait.until(EC.element_to_be_clickable((By.LINK_TEXT, '»')))
    # next_page_button.click()

time.sleep(1)

# print(ffdriver.)
ffdriver.quit()