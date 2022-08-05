import time
import logging
import urllib3
import datetime
import _quotes_checker as qch
'''=================================================================================================================='''
MT5_SERVER = '62.173.147.150:443'
MANGER_LOGIN = '1029'
MANGER_PASSWORD = 'dj805dktj85'
urllib3.disable_warnings()
logging.basicConfig(filename='mt5_quotes_checker.log', encoding='utf-8', level=logging.INFO)
logging.info(str(datetime.datetime.now()) + ' - Checker started')

try:
    while True:
        if qch.get_gateway_status(MT5_SERVER, MANGER_LOGIN, MANGER_PASSWORD, 0) == 0:
            logging.error(str(datetime.datetime.now()) + ' - Gateway ERROR')
        time.sleep(60)
except Exception as ex:
    logging.error(f"{ex}\n" + str(datetime.datetime.now()) + " - Script ERROR")
finally:
    logging.info(str(datetime.datetime.now()) + ' - Checker stopped')



