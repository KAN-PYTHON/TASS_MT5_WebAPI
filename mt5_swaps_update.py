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
time_now = str(datetime.datetime.now())
date_now = str(datetime.date.today())
log_name = str('log\log_mt5_swaps_update_' + date_now + '.log')
session = 'Сессия не открыта'
symbols_list = 'Список символов не определён'


# Создаем log файлы для скрипта
if os.path.exists(log_name):
    os.remove(log_name)
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.INFO)

# Получаем html код страницы TopFX и все <td> теги
session = HTMLSession()
content = session.get(TOPFX_LINK)
content.html.render()
content = content.text
soup = BeautifulSoup(content, 'lxml')
soup_td = soup.find_all('td')

# Открываем сессию с MT5 и получаем список символов и убираем из него CFD
try:
    session = MT5.connect(MT5_SERVER, MANGER_LOGIN, MANGER_PASSWORD)
    symbols_list = session.get('https://' + MT5_SERVER + '/api/symbol/list')
    symbols_list = symbols_list.json().get('answer')
    logging.info(time_now + ' ' + 'Подключение к серверу: ' + str(session.verify))
except Exception:
    logging.error(time_now + ' ' + 'Ошибка подключения к серверу: ' + str(session))
    print('Ошибка подключения к серверу:', str(session))
    exit()

# Приводим в порядок список символов, удаляем лишние и сортируем
i = 0
while i < len(symbols_list):
    symbol = session.get('https://' + MT5_SERVER + '/api/symbol/get?symbol='+symbols_list[i])
    path = symbol.json().get('answer').get('Path')
    digits = symbol.json().get('answer').get('Digits')
    if ('Forex' not in path) and ('Commodities' not in path) and (symbols_list[i] not in soup_td):
        symbols_list.pop(i)
        i += -1
    i += 1
symbols_list.sort()

# Формируем список значений свопов символов с TopFX из html кода
swaps_list = []
i = 0
while i < len(soup_td)-3:
    if soup_td[i].text in symbols_list:
        swaps_list.append(soup_td[i].text)
        swaps_list.append(soup_td[i+3].text)
        swaps_list.append(soup_td[i+4].text)
    i += 1

# Модифицируем swaps в списке swaps_list с поправкой на Digits
i = 0
while i < len(swaps_list)-3:
    if swaps_list[i] in symbols_list:
        symbol = session.get('https://' + MT5_SERVER + '/api/symbol/get?symbol=' + swaps_list[i])
        digits = int(symbol.json().get('answer').get('Digits'))
        swap_long = round(round(float(swaps_list[i+1]), 5)*(10**digits)/10, 1)
        swap_short = round(round(float(swaps_list[i + 2]), 5)*(10**digits)/10, 1)

        if (swap_long > 0) and (swap_short > 0):    # Если оба положительные делаем их отрицательными
            swap_long = -swap_long
            swap_short = -swap_short
        if(swap_long > 0) and (swap_short < 0):   # Если swap_long > 0 и swap_short < 0
            swap_long = swap_long + swap_short
            swap_short = swap_short * 2
        if (swap_long < 0) and (swap_short > 0):  # Если swap_long < 0 и swap_short > 0
            swap_short = swap_short + swap_long
            swap_long = swap_long * 2
        if swap_long == 0:                        # Если swap_long == 0
            swap_long = -0.1
        if swap_short == 0:                       # Если swap_short == 0
            swap_short = -0.1

        print(swaps_list[i], swaps_list[i+1], swaps_list[i+2], 'Digits:', digits)
        swaps_list[i+1] = str(round(swap_long, 2))
        swaps_list[i+2] = str(round(swap_short, 2))
        print(swaps_list[i], swaps_list[i+1], swaps_list[i+2], 'Digits:', digits)

        # Получаем свойства символа по индексу в json /api/symbol/get?symbol= и модифицируем /api/symbol/add?
        try:
            symbol_property = session.get('https://' + MT5_SERVER + '/api/symbol/get?symbol=' + swaps_list[i])
            symbol_property = symbol_property.json()
            symbol_property['answer']['SwapLong'] = swaps_list[i+1]
            symbol_property['answer']['SwapShort'] = swaps_list[i+2]
            symbol_property = json.dumps(symbol_property['answer'])
            symbol_update = ''
            symbol_update = session.post('https://' + MT5_SERVER + '/api/symbol/add?', symbol_property)
            logging.info(str(datetime.datetime.now()) + ' ' + swaps_list[i] + ' -> long: ' + swaps_list[i + 1] +
                         ' short: ' + swaps_list[i + 2] + ' -> OK')
        except Exception:
            logging.error(' Can\'t get the symbol property, ID: ' + str(i) + swaps_list[i])
            i += 1
            continue
    i += 1



# while i < symbols_total:
#     # /api/symbol/next?index= - Get Symbol properties by index
#     try:
#         symbol_property = session.get('https://' + MT5_SERVER + '/api/symbol/next?index=' + str(i))
#     except Exception:
#         logging.error(' Can\'t get the symbol property, ID: ' + str(i))
#         i += 1
#         continue
#
#     retcode = symbol_property.json().get('retcode')
#     answer = symbol_property.json().get('answer')
#
#     if retcode == "0 Done" and len(answer) != 0:
#         symbol_name = str(symbol_property.json().get('answer')['Symbol'])
#         # symbol_name = mt5.url_decode_simbols(symbol_name)
#     else:
#         logging.error('Can\'t get the symbol name, ID: ' + str(i))
#         i += 1
#         continue
#
#     # /api/tick/last - Get Symbol prices by name
#     try:
#         symbol_price = session.get('https://' + MT5_SERVER + '/api/tick/last?symbol=' + symbol_name + '&trans_id=0')
#     except Exception:
#         logging.error('Can\'t get the symbol price, ID: ' + str(i) + '; ' + symbol_name)
#         i += 1
#         continue
#
#     retcode = symbol_price.json().get('retcode')
#     answer = symbol_price.json().get('answer')
#
#     if retcode == "0 Done" and len(answer) != 0:
#         symbol_path = symbol_property.json().get('answer')['Path']
#         if symbol_path.find(SYMBOL_SUBSTR) < 0:
#             logging.error('Symbol skipped, ID: ' + str(i) + '; ' + symbol_path)
#             i += 1
#             continue
#
#         symbol_digits = symbol_property.json().get('answer')['Digits']
#         symbol_ask = float(symbol_price.json().get('answer')[0]['Ask'])
#         symbol_bid = float(symbol_price.json().get('answer')[0]['Bid'])
#         symbol_spread = int((symbol_ask - symbol_bid) * (10 ** int(symbol_digits)))
#
#         if symbol_spread == 0:
#             logging.info('Symbol spread error, ID: ' + str(i) + '; ' + symbol_name)
#             logging.error('Symbol spread error, ID: ' + str(i) + '; ' + symbol_path)
#             i += 1
#             continue
#         logging.info(symbol_name + '/' + str(symbol_digits) + '/' + str(symbol_bid) + '/' + str(symbol_ask))
#
#         # Formation of new parameters to json
#         symbol_property = symbol_property.json()
#         symbol_property['answer']['FilterSoft'] = str(symbol_spread * 10)
#         symbol_property['answer']['FilterSoftTicks'] = '2'
#         symbol_property['answer']['FilterHard'] = str(symbol_spread * 20)
#         symbol_property['answer']['FilterHardTicks'] = '3'
#         symbol_property['answer']['FilterDiscard'] = str(symbol_spread * 100)
#         symbol_property = json.dumps(symbol_property['answer'])
#
#         # Update symbols params
#         symbol_update = ''
#         try:
#             symbol_update = session.post('https://' + MT5_SERVER + '/api/symbol/add?', symbol_property)
#         except Exception:
#             logging.error('Can\'t get update the symbol, ID: ' + str(i) + '; ' + symbol_path)
#             i += 1
#             continue
#
#         retcode = symbol_update.json().get('retcode')
#         answer = symbol_update.json().get('answer')
#
#         if retcode == "0 Done" and len(answer) != 0:
#             logging.info('Update, ID: ' + str(i) + '; ' + symbol_name + ' (' +
#                              str(symbol_spread) + '/' +
#                              str(symbol_spread * 10) + '/' +
#                              str(symbol_spread * 20) + '/' +
#                              str(symbol_spread * 100) + ')' + ' -> Ok')
#             updated_count += 1
#         else:
#             logging.error('Update error, ID: ' + str(i) + '; ' + symbol_path)
#             i += 1
#             continue
#     else:
#         logging.error('Request price error, ID: ' + str(i) + '; ' + symbol_name)
#         i += 1
#         continue
#     i += 1


# print(content)
# print(symbols_list)
# print(swaps_list)
# print(soup_td)
