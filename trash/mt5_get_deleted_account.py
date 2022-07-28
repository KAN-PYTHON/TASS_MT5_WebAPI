import os
import logging
import datetime
import urllib3
from lib import mt5_webapi_lib as mt5

urllib3.disable_warnings()

# Constants of MT5 Server
MT5_SERVER = '62.173.147.150:443'
MANGER_LOGIN = '1029'
MANGER_PASSWORD = 'dj805dktj85'

# Создаем log файлы для скрипта
log_name = str('log\log_mt5_get_deleted_' + str(datetime.date.today()) + '.log')
if os.path.exists(log_name):
    os.remove(log_name)
logging.basicConfig(filename=log_name, encoding='utf-8', level=logging.INFO)

# Устанавливаем соединение с MT5
try:
    session = mt5.connect(MT5_SERVER, MANGER_LOGIN, MANGER_PASSWORD)
    logging.info(str(datetime.datetime.now()) + ' MT5 session: ' + str(session.verify))
    #print(' MT5 session: ' + str(session.verify))
except Exception:
    logging.error('Can\'t open MT5 session' + str(session.verify))
    exit()

# Устанавливаем соединение с MT5
i = 10000
while i < 10100:
    try:
        account_property = session.get('https://' + MT5_SERVER + '/api/user/archive/get?login=' + str(i))
        if account_property.json().get('retcode') == "0 Done":
            print('Account:', i, account_property.json().get('answer'))

        #logging.info(str(datetime.datetime.now()) + ' MT5 session: ' + str(session.verify))
    except Exception:
        logging.error('Can\'t open MT5 session' + str(session.verify))
        exit()
    i += 1
