import os
import time
import re
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.common.by import By

#chrome_options = ArgOptions()
#chrome_options.add_argument(f"user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
#chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#chrome_options.add_argument("--headless") 


#price = browser.find_elements(By.CSS_SELECTOR, '[class="ty-price"]')

def parser_one_pages(browser):
    data = []
    products = browser.find_elements(By.CSS_SELECTOR, '[class="ty-column5"]')
    for product in products:
        element_of_data = []
        full_name = product.find_element(By.CSS_SELECTOR, '[class="ut2-gl__name"]')
       # group = re.search(r"\W+", full_name.text)
       # group = group[0].replace("-", "")
       # name = full_name.text.replace(group, "")
        price = product.find_element(By.CSS_SELECTOR, '[class="ty-price"]')
        full_availability = product.find_element(
            By.CSS_SELECTOR, '[class="ty-control-group ty-sku-item cm-hidden-wrapper"]')
        availability = re.split(r"\W+", full_availability.text)
        availability = availability[2] + " " + availability[3]
        element_of_data.append(full_name.text + " Цена: ")
       # element_of_data.append(group)
        element_of_data.append(price.text + " ")
        element_of_data.append(availability)
        data.append(element_of_data)
        #print(price.text + name.text + availability.text)
    return data

url = 'https://stomdevice.ru/vse-tovary/page-'
data = []
pages = 1
out_file = open("data.csv", 'w+')
while pages!=4:
    browser = webdriver.Chrome()
    full_url = url + str(pages) + "/"
    browser.get(full_url)
    for i in parser_one_pages(browser):
        out_file.writelines(i)
        out_file.write("\n")
    pages+=1
out_file.close()
time.sleep(5)
browser.close()
