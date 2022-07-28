import os
import logging
import datetime
import urllib3
import time
from datetime import timedelta
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
    logging.info(' MT5 session: ' + str(session.verify))
    #print(' MT5 session: ' + str(session.verify))
except Exception:
    logging.error('Can\'t open MT5 session' + str(session.verify))
    exit()

# /api/daily_get?from=дата&to=дата&login=логин
# today = datetime.datetime.today()
# yesterday = datetime.datetime.today()
today = datetime.datetime.today() - timedelta(days=5)
yesterday = datetime.datetime.today() - timedelta(days=5)

print(today)
print(yesterday)

today = int(datetime.datetime.timestamp(today))
yesterday = int(datetime.datetime.timestamp(yesterday))



print('1585904106', datetime.datetime.fromtimestamp(1585904106))
print('1658417311', datetime.datetime.fromtimestamp(1658417311))
print('1658417311', datetime.datetime.fromtimestamp(1658417311))
print(today)
print(yesterday)
today = '2022-07-26 23:59:59.000000'
today = datetime.datetime.strptime(today, '%Y-%m-%d %H:%M:%S.%f')
yesterday = '2022-07-01 23:59:59.000000'
yesterday = datetime.datetime.strptime(yesterday, '%Y-%m-%d %H:%M:%S.%f')

print('Ooooo!', yesterday, today)

today = int(datetime.datetime.timestamp(today))
yesterday = int(datetime.datetime.timestamp(yesterday))

# /api/daily_get_light?from=дата&to=дата&login=логин
# https://62.173.147.150:443/api/daily_get_light?from=1658858399&to=1656698399&login=1573


link = 'https://' + MT5_SERVER + '/api/daily_get_light?from='+str(yesterday)+'&to='+str(today)+'&login='+'1425'
# link = 'https://' + MT5_SERVER + '/api/daily_get?from='+'2022-07-25'+'&to='+'2022-07-25'+'&login='+'1573'
# link = 'https://' + MT5_SERVER + '/api/daily_get?from=1658848468&to=1658762068&login=1573'

print(link)
daily_report = session.get(link)
print(daily_report.json())




# print('today', today)
# print('yesterday', yesterday)
# print(datetime.datetime.timestamp(today))
# print(datetime.datetime.timestamp(yesterday))

# print(time.time())
# print(datetime.datetime.fromtimestamp(time.time()))
# print(datetime.datetime.timestamp(datetime.datetime.today()))

# print(today)
# print(today.ctime())
# print("Today is: ", datetime.datetime.timestamp(today))

# # Yesterday date
# yesterday = today - timedelta(days=1)
# print("Yesterday was: ", yesterday)