import requests
from bs4 import BeautifulSoup
import json


url = 'https://oriencoop.cl/sucursales.htm'

req = requests.get(url)
src = req.text
soup = BeautifulSoup(src, 'lxml')
all_shops_hrefs = soup.find(class_='c-left').find_all('a')

#Забераем общие телефоны с главной страницы
shared_phones_urls = soup.find(class_='b-call shadow').find_all('a')
first_shared_phone = shared_phones_urls[0].text.replace(' ', '')
second_shared_phone = shared_phones_urls[1].text.replace(' ', '')

#Формируем список адресов конкретных магазинов, чтобы обращаться к ним из файла.
with open('oriencoop_shop_hrefs.txt', 'w') as file:
    for item in all_shops_hrefs:
        if item.get('href')[0] == '/':
            file.write(f'https://oriencoop.cl{item.get("href")}\n')

result = []
with open('oriencoop_shop_hrefs.txt') as file:
    lines = [line.strip() for line in file.readlines()]
    for line in lines:
        url = line
        req = requests.get(url)
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        all_data = soup.find(class_='s-dato').find_all('span')
        maps_data = soup.find(class_='s-mapa')
        cordinates = maps_data.iframe.get('src').split('!2d')[1].split('!3d')
        longitude = cordinates[0]
        latitude = cordinates[1].split('!')[0]
        clear_data = {
            'address': all_data[0].text,
            "latlon": [],
            "name": "Oriencoop",
            "phones": [],
            "working_hours": []
        }
        clear_data['phones'].append(all_data[1].text.replace('-', ''))
        clear_data['phones'].append(first_shared_phone)
        clear_data['phones'].append(second_shared_phone)
        start_work_time = all_data[3].text[9:14].replace('.', ':').strip()
        start_lunch_time = all_data[3].text[16:22].replace('.', ':').strip()
        start_after_lunch = all_data[4].text[8:13].replace('.', ':').strip()
        end_of_work_mon_thu = all_data[4].text[16:21].replace('.', ':').strip()
        end_of_work_fri = all_data[4].text[43:49].replace('.', ':').strip()
        clear_data['working_hours'].append(f'mon-thu {start_work_time}-{start_lunch_time} {start_after_lunch}-{end_of_work_mon_thu}')
        clear_data['working_hours'].append(f'fri {start_work_time}-{start_lunch_time} {start_after_lunch}-{end_of_work_fri}')
        clear_data['latlon'].append(float(latitude))
        clear_data['latlon'].append(float(longitude))
        result.append(clear_data)

with open('oriencoop_shops.json', 'w', encoding="utf-8") as file:
    json.dump(result, file, indent=4, ensure_ascii=False)
