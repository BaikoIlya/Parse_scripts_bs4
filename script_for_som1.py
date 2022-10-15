import requests
from bs4 import BeautifulSoup
import json

#Так как сайт, отдаёт по 1 ссылке на запрос, руками создал файл со ссылками на магазины.

result = []
with open('som1_shops_href.txt') as file:
    lines = [line.strip() for line in file.readlines()]
    for line in lines:
        clear_data = {
            'address': '',
            "latlon": [],
            "name": "",
            "phones": [],
            "working_hours": []
        }
        url = line
        req = requests.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"
                }
            )
        src = req.text
        soup = BeautifulSoup(src, 'lxml')
        scripts = soup.find_all('script')
        cords = scripts[55].text.split("['")[1]
        latitude = cords.split("','")[0]
        longitude = cords.split("','")[1].split("']")[0]
        container = soup.find(class_='page-body').find(class_='container')
        shop_name = container.find('h1').text
        shop_detail = container.find(class_='shop-detail-block').find_all('td')
        shared_phone = soup.find(class_='phone-footer').text.replace('-', '')
        shop_address = shop_detail[2].text
        shop_phone = shop_detail[5].text.replace('-', '').replace('(', '').replace(')', '').replace(' ', '').split(',')[-1]
        shop_working_time = shop_detail[8].text
        if ',' in shop_working_time:
            days = shop_working_time.split(',')
            clear_data['working_hours'].append(days[0].strip())
            clear_data['working_hours'].append(days[1].strip())
        else:
            clear_data['working_hours'].append(shop_working_time)
        clear_data['address'] = shop_address
        clear_data['latlon'].append(float(latitude))
        clear_data['latlon'].append(float(longitude))
        clear_data['name'] = shop_name
        clear_data['phones'].append(shared_phone)
        if shared_phone not in shop_phone:
            clear_data['phones'].append(shop_phone)
        result.append(clear_data)

with open('som1_shops.json', 'w', encoding="utf-8") as file:
    json.dump(result, file, indent=4, ensure_ascii=False)
