from selenium import webdriver
from bs4 import BeautifulSoup
# from urllib.parse import urljoin
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urljoin
import constants
import os


def connectToStaticWebSite(url, ignoreTerm=None):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    content = driver.page_source
    driver.close()
    soup = BeautifulSoup(content, features="html.parser")
    return soup

def connectToWebsiteWithCheckBox(url, filePath):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("disable-gpu")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--log-level=3')
    options.add_argument("download.default_directory={}".format(constants.tempDownloadPath))
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    content_list = driver.find_element_by_id("notebook_list")
    items_list = content_list.find_elements_by_class_name("list_item")
    folder_list = []
    if len(items_list) > 1:
        for item in items_list[1:]:
            try:
                _ = item.find_element_by_class_name("folder_icon")
                linkHTML = item.find_element_by_class_name("item_link")
                temp = ExtractLink(linkHTML)
                folder_list[temp[0]] = temp[1]
            except NoSuchElementException:
                try:
                    _ = item.find_element_by_class_name("notebook_icon")
                    box = item.find_element_by_xpath("//input[@type='file']")

    try:
        counter = 0
        while counter < 10:
            btn = driver.find_element_by_id("notebook_list")
            btn.click()
            counter+=1
    except NoSuchElementException:
        pass
    content = driver.page_source
    driver.close()
    soup = BeautifulSoup(content, features="html.parser")
    return soup

def ExtractLink(url, content):
    temp = content.find('a', href=True)
    href = urljoin(url, temp['href'])
    name = content.find('span', attrs={'class': 'item-name'}).get_text()
    return name, href