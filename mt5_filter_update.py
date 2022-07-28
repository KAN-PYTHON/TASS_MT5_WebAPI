"""
Скрипт устанавливает уровни фильтрации котировок на основании размеров спрэда
"""
import os
import datetime
import json
import urllib3
import logging
from lib import mt5_webapi_lib as mt5

urllib3.disable_warnings()

# Constants of MT5 Server
MT5_SERVER = '62.173.147.150:443'
MANGER_LOGIN = '1029'
MANGER_PASSWORD = 'dj805dktj85'
time_now = str(datetime.datetime.now())
date_now = str(datetime.date.today())

# Создаем log файлы для скрипта
log_name = str('log\log_mt5_filter_update_' + str(datetime.date.today()) + '.log')
if os.path.exists(log_name):
    os.remove(log_name)
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.INFO)

# Открываем соединение с MT5 и получаем список символов
# '/api/symbol/list' - Get symbol`s list
# /api/symbol/total - Get symbols count total
try:
    session = mt5.connect(MT5_SERVER, MANGER_LOGIN, MANGER_PASSWORD)
    symbols_list = session.get('https://' + MT5_SERVER + '/api/symbol/list')
    symbols_total = session.get('https://' + MT5_SERVER + '/api/symbol/total')
    symbols_list = symbols_list.json().get('answer')
    symbols_total = symbols_total.json().get('answer')
    logging.info(str(datetime.datetime.now()) + ' Symbols total: ' + str(symbols_total))
    print('Всего символов:', symbols_total)
except Exception:
    logging.error('Can\'t get the count of symbols')
    exit()

# Получаем данные по символу, вычисляем уровень фильтрации, обновляем символы
i = 0
updated_count = 0
print('Обработка символов начата в :', str(datetime.datetime.now()))
while i < len(symbols_list):
    # /api/symbol/next?index= - Get Symbol properties by index
    try:
        symbol_property = session.get('https://' + MT5_SERVER + '/api/symbol/get?symbol=' + symbols_list[i])
        symbol_price = session.get('https://' + MT5_SERVER + '/api/tick/last?symbol=' + symbols_list[i] + '&trans_id=0')
        symbol_digits = symbol_property.json().get('answer')['Digits']
        symbol_ask = float(symbol_price.json().get('answer')[0]['Ask'])
        symbol_bid = float(symbol_price.json().get('answer')[0]['Bid'])
        symbol_spread = round((symbol_ask - symbol_bid) * (10 ** int(symbol_digits)), 0)
        symbol_property = symbol_property.json()
        symbol_property['answer']['FilterSoft'] = str(symbol_spread * 5)
        symbol_property['answer']['FilterSoftTicks'] = '2'
        symbol_property['answer']['FilterHard'] = str(symbol_spread * 10)
        symbol_property['answer']['FilterHardTicks'] = '3'
        symbol_property['answer']['FilterDiscard'] = str(symbol_spread * 50)
        symbol_property = json.dumps(symbol_property['answer'])
        symbol_update = session.post('https://' + MT5_SERVER + '/api/symbol/add?', symbol_property)
        logging.info(symbols_list[i] + ' / symbol_filter = ' + str(symbol_spread) + ' / ' +
                     str(symbol_spread * 5) + ' / ' +
                     str(symbol_spread * 10) + ' / ' +
                     str(symbol_spread * 50) + ' -> OK')
        updated_count += 1
    except Exception:
        logging.error(' Can\'t update the symbol property, ID: ' + symbols_list[i])
        i += 1
        continue
    i += 1

session.close()
logging.info('\n' + 'END at ' + str(datetime.datetime.now()) + '\n' + 'Updated symbols: ' + str(updated_count) + '\n')
print('Обработка символов завершена в :', str(datetime.datetime.now()))
print('Обновлено символов :', str(updated_count))
