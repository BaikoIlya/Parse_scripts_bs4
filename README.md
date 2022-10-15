## Описание:
Скрипты для сбора данных о магазинах и формарования json файлов.

### Установка:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:BaikoIlya/RocketData_test.git
```

```
cd RocketData_test
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

C запущенным виртуальным окружением, запускайте скрипты.

###P.S. Для скрипта script_for_naturasiberica.py нужен ключ Yandex JavaScript API и HTTP Геокодер. Или закоментируйте строки для добавляения коррдинат.