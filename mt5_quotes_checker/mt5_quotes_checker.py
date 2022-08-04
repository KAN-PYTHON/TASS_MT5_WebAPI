import time
import logging
import urllib3
import datetime
from lib import mt5_webapi_lib as mt5


def get_gateway_status(gate_index):
    MT5_SERVER = '62.173.147.150:443'
    MANGER_LOGIN = '1029'
    MANGER_PASSWORD = 'dj805dktj85'
    result = 0

    # Открываем соединение с MT5 и получаем список символов
    # '/api/gateway/next?index=0' - Получение шлюза по индексу
    try:
        session = mt5.connect(MT5_SERVER, MANGER_LOGIN, MANGER_PASSWORD)
        gateway_config = session.get('https://' + MT5_SERVER + '/api/gateway/next?index=' + str(gate_index))
        result = int(gateway_config.json().get('answer')['State']['BytesReceived'])
    except Exception as ex:
        print(f"{ex}\nERROR MT5 Server no connection!")
    finally:
        return result


'''=================================================================================================================='''
urllib3.disable_warnings()
logging.basicConfig(filename='mt5_quotes_checker.log', encoding='utf-8', level=logging.INFO)
logging.info(str(datetime.datetime.now()) + ' Checker started')

try:
    while True:
        if get_gateway_status(0) == 0:
            logging.error(str(datetime.datetime.now()) + ' - Gateway ERROR')
        time.sleep(10)
except Exception as ex:
    logging.error(f"{ex}\n" + str(datetime.datetime.now()) + " - Script ERROR")
finally:
    logging.info(str(datetime.datetime.now()) + ' Checker stopped')



