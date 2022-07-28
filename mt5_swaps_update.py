"""
Скрипт устанавливает swaps согласно данных -TopFX по Forex и в процентах по Indices и crypto
"""

import os
import json
import urllib3
import logging
import datetime
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from lib import mt5_webapi_lib as MT5

urllib3.disable_warnings()

# Constants of MT5 Server
MT5_SERVER = '62.173.147.150:443'
MANGER_LOGIN = '1029'
MANGER_PASSWORD = 'dj805dktj85'
TOPFX_LINK = 'https://swap.topfx.com.sc/en/swap/institutional-rates/2022-07-20'
log_name = str('log\log_mt5_swaps_update_' + str(datetime.date.today()) + '.log')
session = 'Сессия не открыта'
symbols_list = 'Список символов не определён'


# Создаем log файлы для скрипта
if os.path.exists(log_name):
    os.remove(log_name)
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.INFO)

# Начинаем парсинг страницы TopFX, берём все <td> теги
print('Начинаем парсинг TopFX ...', str(datetime.datetime.now()))
session = HTMLSession()
content = session.get(TOPFX_LINK)
content.html.render()
content = content.text
session.close()
soup = BeautifulSoup(content, 'lxml')
soup_td = soup.find_all('td')
i = 0
soup_list = []
while i < len(soup_td):
    soup_list.append(soup_td[i].text)
    i += 1
print('Парсинг завершен ... ', str(datetime.datetime.now()))

# Получаем список символов MT5
try:
    session = MT5.connect(MT5_SERVER, MANGER_LOGIN, MANGER_PASSWORD)
    symbols_list = session.get('https://' + MT5_SERVER + '/api/symbol/list')
    symbols_list = symbols_list.json().get('answer')
except Exception:
    logging.error(str(datetime.datetime.now()) + ' ' + 'Ошибка подключения к серверу: ' + str(session))
    quit()

# Формируем список значений свопов символов из html кода
i = 0
forex_list = []
indices_list = []
crypto_list = []
while i < len(symbols_list):
    # Получаем данные о символе из MT5
    symbol_property = session.get('https://' + MT5_SERVER + '/api/symbol/get?symbol=' + symbols_list[i])
    path = symbol_property.json().get('answer').get('Path')
    digits = float(symbol_property.json().get('answer').get('Digits'))

    # Обновление символов типа Forex и Commodities
    if ('Forex' in path) or ('Commodities' in path):
        forex_list.append(symbols_list[i])
        if symbols_list[i] in soup_list:
            swap_long = str(-abs(round(float(soup_td[soup_list.index(symbols_list[i])+3].text)*(10**digits), 1)))
            swap_short = str(-abs(round(float(soup_td[soup_list.index(symbols_list[i])+4].text)*(10**digits), 1)))
            forex_list.append(swap_long)
            forex_list.append(swap_short)
        else:
            swap_long = '0'
            swap_short = '0'
            forex_list.append(swap_long)
            forex_list.append(swap_short)
        try:
            symbol_property = symbol_property.json()
            symbol_property['answer']['SwapMode'] = '1'
            symbol_property['answer']['SwapLong'] = swap_long
            symbol_property['answer']['SwapShort'] = swap_short
            symbol_property = json.dumps(symbol_property['answer'])
            symbol_update = session.post('https://' + MT5_SERVER + '/api/symbol/add?', symbol_property)
            logging.info(str(datetime.datetime.now()) + ' ' + path + ' -> long: ' + swap_long +
                         ' short: ' + swap_short + ' -> OK')
        except Exception:
            logging.error(' Can\'t get the symbol property, ID: ' + str(i) + path)
            i += 1
            continue
        print(path, swap_long, swap_short)

    # Обновление символов типа Indices
    if 'Indices' in path:
        swap_long = '-10'
        swap_short = '-10'
        indices_list.append(symbols_list[i])
        indices_list.append(swap_long)
        indices_list.append(swap_short)
        try:
            symbol_property = symbol_property.json()
            symbol_property['answer']['SwapMode'] = '5'
            symbol_property['answer']['SwapLong'] = swap_long
            symbol_property['answer']['SwapShort'] = swap_short
            symbol_property = json.dumps(symbol_property['answer'])
            symbol_update = session.post('https://' + MT5_SERVER + '/api/symbol/add?', symbol_property)
            logging.info(str(datetime.datetime.now()) + ' ' + path + ' -> long: ' + swap_long +
                         ' short: ' + swap_short + ' -> OK')
        except Exception:
            logging.error(' Can\'t get the symbol property, ID: ' + str(i) + path)
            i += 1
            continue
        print(path, swap_long, swap_short)

    # Обновление символов типа Crypto
    if 'Crypto' in path:
        swap_long = '-20'
        swap_short = '-20'
        crypto_list.append(symbols_list[i])
        crypto_list.append(swap_long)
        crypto_list.append(swap_short)
        try:
            symbol_property = symbol_property.json()
            symbol_property['answer']['SwapMode'] = '5'
            symbol_property['answer']['SwapLong'] = swap_long
            symbol_property['answer']['SwapShort'] = swap_short
            symbol_property = json.dumps(symbol_property['answer'])
            symbol_update = session.post('https://' + MT5_SERVER + '/api/symbol/add?', symbol_property)
            logging.info(str(datetime.datetime.now()) + ' ' + path + ' -> long: ' + swap_long +
                         ' short: ' + swap_short + ' -> OK')
        except Exception:
            logging.error(' Can\'t get the symbol property, ID: ' + str(i) + path)
            i += 1
            continue
        print(path, swap_long, swap_short)

    i += 1
print(forex_list)
print(indices_list)
print(crypto_list)
