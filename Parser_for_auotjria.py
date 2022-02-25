import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import lxml

driver = webdriver.Chrome()
json_dict= {}
for _ in range(30) :
    url = f"https://auto.ria.com/search/?indexName=auto&country.import.usa.not=-1&price.currency=1&abroad.not=0&custom.not=1&page={_}&size=20"
    src = requests.get(url).text
    soup = BeautifulSoup(src, "lxml")
    address_list = soup.findAll(class_='address')
    for address_elem in address_list:
        try:
            link = address_elem.get('href')
            address_name = address_elem.text
            page_src = requests.get(link).text
            page_soup = BeautifulSoup(page_src, 'lxml')
            name_seller = page_soup.find(class_="seller_info_name bold")
            if name_seller == None:
                name_seller_text = "Нет имени"
            else:
                name_seller_text = name_seller.text
            driver.get(link)
            driver.find_element(By.XPATH, '//*[@id="phonesBlock"]/div/span/a').click()
            phone_num = page_soup.find(class_="popup-successful-call-desk size24 bold green mhide green").text
            json_dict[address_name] = {}
            json_dict[address_name]["Ссылка"] = link
            json_dict[address_name]["Имя"]  = name_seller_text
            json_dict[address_name]["номер"] = phone_num
        except:
            print('Товар продан')
with open("save_json.json", "a", encoding="utf-8") as file:
    file.write(json.dumps(json_dict, indent=4, ensure_ascii=False, sort_keys=True))
