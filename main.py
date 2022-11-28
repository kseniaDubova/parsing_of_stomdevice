
import time
import re
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By


def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя'), number=set('0123456789,- ')):
    name = ""
    group = ""
    flag = 0
    for simvol in text:
        if alphabet.isdisjoint(simvol.lower()) and flag == 0:
            name = name + simvol
        else:
            flag = 1
            group = group + simvol
    return name, group


def parser_one_pages(browser):
    data = []
    products = browser.find_elements(By.CSS_SELECTOR, '[class="ty-column5"]')
    for product in products:
        element_of_data = []
        full_name = product.find_element(
            By.CSS_SELECTOR, '[class="product-title"]')
        name, group = match(full_name.text)
        name = name.replace("-", "")
        try:
            price = product.find_element(By.CSS_SELECTOR, '[class="ty-price"]')
        except:
            price = product.find_element(By.CSS_SELECTOR, '[class="ty-no-price"]')
        full_availability = product.find_element(
            By.CSS_SELECTOR, '[class="ty-control-group ty-sku-item cm-hidden-wrapper"]')
        availability = re.split(r"\W+", full_availability.text)
        availability = availability[2] + " " + availability[3]
        element_of_data.append(name)
        element_of_data.append(group)
        element_of_data.append(price.text)
        element_of_data.append(availability)
        data.append(element_of_data)
    return data


url = 'https://stomdevice.ru/vse-tovary/page-'
end = '/?items_per_page=160'
data = []
pages = 1
out_file = open("data.csv", 'w+')
writer = csv.writer(out_file)
writer.writerow(("Название", "Группа товара", "Цена", "Наличие"))
while pages < 61:
    browser = webdriver.Chrome()
    full_url = url + str(pages) + end
    browser.get(full_url)
    for i in parser_one_pages(browser):
        writer.writerow(i)
    pages += 1
    time.sleep(2)
    browser.close()
    if pages==60:
        break
out_file.close()

