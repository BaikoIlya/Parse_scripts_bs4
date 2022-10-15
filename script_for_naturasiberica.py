import requests
import json
from decimal import Decimal
from yandex_geocoder import Client

#Клиент яндекс декодера для определения координат по адресу.
client = Client()


url = 'https://naturasiberica.ru/local/php_interface/ajax/getShopsData.php?'

#Этот запрос возвращает все данные по магазинам в формате Json.
req = requests.post(
    url,
    headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "BITRIX_SM_GUEST_ID=12142987; BITRIX_SM_LAST_VISIT=15.10.2022+11%3A07%3A59; BITRIX_CONVERSION_CONTEXT_s1=%7B%22ID%22%3A2%2C%22EXPIRE%22%3A1665871140%2C%22UNIQUE%22%3A%5B%22conversion_visit_day%22%5D%7D; BX_USER_ID=ffa46d77a4fc1381194ba3a1e53aa01c; _ga=GA1.2.373386644.1665750666; _gid=GA1.2.1831494381.1665750666; _ym_uid=1665750666625708834; _ym_d=1665750666; PHPSESSID=rabgsepr466f49nh26k5trh2b1; _ym_visorc=w; _ym_isad=2; _gat=1",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "X-Requested-With": "XMLHttpRequest"
    },
    data={
        "type": 'all',
        "active": "natura-siberica-moskva-trts-metropolis"
    }
)
#Так как слишком много вариантов заполнения времени захардкодил все варианты, чтобы всегда был результат как в образце.
working_time_variation = {
    'с 10.00-23.00': ['пн-вс 10:00-23:00'],
    'ежедневно с 10:30-21:30': ['пн-вс 10:30-21:30'],
    'from 09 a.m 21 p.m., from Monday to Saturday': ['пн-вс 9:00-21:00'],
    'from 10 a.m. till 10 p.m., 7 days a week': ['пн-вс 10:00-22:00'],
    'с 10.00-22.00\r\n\r\n': ['пн-вс 10:00-22:00'],
    'с 10.00-21.00': ['пн-вс 10:00-21:00'],
    'с 10.00 до 22.00': ['пн-вс 10:00-22:00'],
    'с 10.00-22.00': ['пн-вс 10:00-22:00'],
    'с 10.00-22.00\r\nВ магазине есть спа-кабинет. ': ['пн-вс 10:00-22:00'],
    'Пн-Вс: 10-22': ['пн-вс 10:00-22:00'],
    'с 09.00-19.00': ['пн-вс 9:00-19:00'],
    'с 10:00 до 19:30': ['пн-вс 10:00-19:30'],
    'Пн.- Пт., с 10.00-18.00': ['пн-пт 10:00-18:00'],
    'с 10:00 до 23:00 часов с воскресенья по четверг,\r\nс 10:00 до 00:00 в пятницу, субботу и в праздничные дни.': ['вс-чт 10:00-23:00', 'пт-сб 10:00-00:00'],
    'Пн-Чт, Вс: 10.00-23.00\r\nПт, Сб: 10.00-00.00 \r\nВ магазине есть спа-кабинет.': ['вс-чт 10:00-23:00', 'пт-сб 10:00-00:00'],
    'с 10.00-22.00\r\nВ магазине есть спа-кабинет.': ['пн-вс 10:00-22:00'],
    'Пн-Чт, Вс: 10.00-22.00\r\nПт, Сб: 10.00-23.00 ': ['вс-чт 10:00-22:00', 'пт-сб 10:00-23:00'],
    'вс-чт\r\n10:00 - 22:00\r\nпт-сб\r\n10:00 - 23:00 \r\n': ['вс-чт 10:00-22:00', 'пт-сб 10:00-23:00'],
    'с 10.00-22.00\r\nВ магазине открыт спа-кабинет. Телефон спа: 8 (495) 692-58-48': ['пн-вс 10:00-22:00'],
    'с 10:00  до 22:00': ['пн-вс 10:00-22:00'],
    'с 10 до 22': ['пн-вс 10:00-22:00'],
    'с 10.00-22.00\r\n': ['пн-вс 10:00-22:00'],
    'Пн-пт: 09:00 - 21:00,\r\nСб: 09:00 - 19:00,\r\nВс: выходной': ['пн-пт 9:00-21:00', 'сб 9:00-19:00'],
    'Пн. - Вск.:10.00 - 22.00': ['пн-вс 10:00-22:00'],
    'Пн - Пт: 08.00-20.00,\r\nСб: 08.00-16.00,\r\nВс: выходной': ['пн-пт 8:00-20:00', 'сб 8:00-16:00'],
    'Пон. - Субб.: 09:00 - 21: 00\r\nВоскр.: 10:00 -  16:00': ['пн-сб 9:00-21:00', 'вс 10:00-16:00'],
    'с 9.00-21.00\r\nВ магазине есть зона СПА. ': ['пн-вс 9:00-21:00'],
    'С 9.00 до 22.00': ['пн-вс 9:00-22:00'],
}

result = []
for el in req.json()['original']:
    clear_data = {
        'adress': '',
        "latlon": [],
        "name": "Natura Siberica",
        "phones": [],
        "working_hours": []
    }
    clear_data['adress'] = f'{el["city"]},{el["address"].replace("&quot;", "")}'
    coordinates = client.coordinates(clear_data['adress']) # Если нет ключа, закомантируйте это.
    clear_data['latlon'].append(float(coordinates[1])) # Если нет ключа, закомантируйте это.
    clear_data['latlon'].append(float(coordinates[0])) # Если нет ключа, закомантируйте это.
    if el['phone'] is not None:
        clear_data['phones'].append(el['phone'].replace('-', '').replace('(', '').replace(')', '').replace(' ', ''))
    if el['schedule'] in working_time_variation:
        clear_data['working_hours'] = working_time_variation[el['schedule']]
    result.append(clear_data)

with open('naturasiberica_shops.json', 'w', encoding="utf-8") as file:
    json.dump(result, file, indent=4, ensure_ascii=False)
