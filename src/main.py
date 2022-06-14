import yaml
import logging.config
import os

from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FFService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

while os.getcwd().split('\\')[-1] != "PP1_scrape_me_home":
    os.chdir('..')

#Loading config file for logging
with open('.\config\config.yml', 'r') as config:
    logging.config.dictConfig(yaml.safe_load(config)['logging'])

main_logger = logging.getLogger('main')
error_logger = logging.getLogger('error')

#Loading config file to get url to scrape
with open('.\config\config.yml', 'r') as config:
    url = yaml.safe_load(config)['urls']

url_to_scrape = url['url']

#Configuring scraper
url = url_to_scrape
op = webdriver.FirefoxOptions()
ffdriver = webdriver.Firefox(service=FFService('src/drivers/geckodriver_v0.31.0.exe'), options=op)

#Opening url to scrape and bypassing accept cookies pop-up
target_button = "button[id*='onetrust-accept-btn-handler']"
ffdriver.get(url)
wait = WebDriverWait(ffdriver, 15)
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, target_button)))
cookies_button = ffdriver.find_element(By.CSS_SELECTOR, target_button)
cookies_button.click()

#Defining scrape method
def get_data():
    rows = ffdriver.find_elements(By.CSS_SELECTOR, '*.list-row')
    data = []

    #Waiting for page to load
    wait.until(EC.text_to_be_present_in_element(
        (By.CSS_SELECTOR, 'tr.search-mark > td > div > div.text'),
        'SKELBIMŲ'))

    #Scraping info
    for row in rows:
        try:
            address = row.find_element(By.CSS_SELECTOR, 'td.list-adress > h3 > a')
            price = row.find_element(By.CSS_SELECTOR, 'td.list-adress > div > span.list-item-price')
            area = row.find_element(By.CSS_SELECTOR, 'td.list-AreaOverall')
        except NoSuchElementException:
            error_logger.exception('No such element to select')
            continue
        #Cleaning address text
        delim = "\\n"
        raw_text = "%r"%address.text
        split_raw = raw_text.split(delim)
        clean_address = ' '.join(split_raw)
        #Defining scraped info structure and adding to list
        data.append({"Address":clean_address, "Price":price.text, "Area":area.text + " m²", "URL":address.get_attribute('href')})

    #Printing scraped info
    for d in data:
        print(d)

#Scraping through pages
while(True):
    get_data()
    try:
        current_page = ffdriver.find_element(By.CSS_SELECTOR, 'a.active-page')
    except NoSuchElementException:
        error_logger.exception('No such element to select')
    try:
        main_logger.info(f'Page {current_page.text} scraped successfully')
    except NameError:
        main_logger.info(f'Page 1 scraped successfully')
    try:
        next_page_button = ffdriver.find_element(By.LINK_TEXT, '»')
    except NoSuchElementException:
        main_logger.info(f'All available pages has been scraped successfully')
        break
    wait.until(EC.element_to_be_clickable((next_page_button)))
    href_data = next_page_button.get_attribute('href')
    if href_data is None:
        main_logger.info(f'All available pages has been scraped successfully')
        break
    else:
        next_page_button.click()

ffdriver.quit()