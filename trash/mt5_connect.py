# Подключение к DEV MT5 TASS FX
#

import os
import datetime
import urllib3
import logging
from lib import mt5_webapi_lib as mt5

# Отключаем лишние уведомления об некритичных ошибках
urllib3.disable_warnings()

# Начальные установки подключения к MT5
time_now = str(datetime.datetime.now())
date_now = str(datetime.date.today())
log_name = str('log\log_' + date_now + '.log')
server = '62.173.147.150:443'
manager = '1029'
password = 'dj805dktj85'

# Создаем log файлы для скрипта
if os.path.exists(log_name):
    os.remove(log_name)
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.INFO)

# Устанавливаем соединение с MT5
try:
    session = mt5.connect(server, manager, password)
    if session.verify:
        logging.info(time_now + ': Сессия успешно открыта')
except Exception as exp:
    logging.error(time_now + ': Ошибка открытия сессии, error:' + str(session) + ' / ' + str(exp))
    exit()

# Отправка запроса на MT5
symbols_total = session.get('https://' + server + '/api/symbol/total')
retcode = symbols_total.json().get('retcode')
symbol_count = int(symbols_total.json().get('answer')['total'])
if symbol_count > 0:
    logging.info(time_now + ': Число символов: ' + symbol_count.__str__())
else:
    logging.error(time_now + ': Ошибка запроса')
    exit()

symbol_property = session.get('https://' + server + '/api/symbol/next?index=' + str(0))
retcode = symbol_property.json().get('retcode')
answer = symbol_property.json().get('answer')

if retcode == "0 Done" and len(answer) != 0:
    symbol_name = str(symbol_property.json().get('answer')['Symbol'])
    print(symbol_name)
    # symbol_name = mt5.url_decode_simbols(symbol_name)
else:
    logging.info('Can\'t get the symbol name, ID: ' + str(1))
    # logging.error('Can\'t get the symbol name, ID: ' + str(1))

print(symbol_name)
