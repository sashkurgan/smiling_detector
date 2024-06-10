import random

import requests
import browser_cookie3
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import re
import time
import html
from bs4 import BeautifulSoup as bs
from civitai import images, tags
import os

output_images_folder = 'not_smiling_images' #output parsed images folder
html_page = "html_pages/synth_not_smiling_page2.html" #html page with images links

def download_image(id, img_url):
    link=img_url
    img = requests.get(link)
    out = open(f"{output_images_folder}/{id}.png", "wb")
    out.write(img.content)
    out.close()

with open(html_page,encoding='utf-8') as file:
    srcs = file.read()
soups=bs(srcs, 'lxml')
imgs_links=(soups.find(class_='mantine-1mlssal')).find_all('a')

chrome_cookies = browser_cookie3.chrome(domain_name='.google.com')
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=C:\\Users\\Admin\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_experimental_option("detach", True)
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

downloaded_imgs=os.listdir(output_images_folder)

for i in range(len(imgs_links)):
    try:
        href=imgs_links[i]['href']
        print(href)
        id=href.split('/')[-1]
        url='https://civitai.com'+href
        if (id + ".png") not in downloaded_imgs:

            driver.get(url=url)
            time.sleep(random.uniform(1.5, 3.5))
            page = (driver.page_source)
            soup = bs(page)
            frame_class = (soup.find(class_= re.compile('max-h-full w-auto max-w-full')))
            img_url = (frame_class["src"])

            download_image(id, img_url)

            time.sleep(random.uniform(2,7))

        else:
            print(f"the element with id {id} is already exist")
            continue

    except:
        print(f"проблема с элементом {i}")
        continue







