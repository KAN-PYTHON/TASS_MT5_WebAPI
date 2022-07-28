# Скрипт SchoolMT5 закрывает счет и блокирует счет при достижении лимита просадки
#
import mt5_webapi_lib as mt5
import time
# Начальные установки подключения к MT5
server = 'webapi.educationvector.com'
manager = '1003'
password = 'hf7jrf83er'

# Получаем значение account из внешней DB
account = '111644'

# Устанавливаем соединение с MT5
session = mt5.connect(server, manager, password)

# Запрещаем торговлю на счету account
mt5.mod_account_rights(server, account, session, 16743)

# Закрываем отложенные ордера
orders_count = mt5.del_order(server, account, session)
if orders_count > 0:
    while orders_count > 0:
        orders_count = mt5.del_order(server, account, session)
        time.sleep(0.5)
# Закрываем открытые позиции
positions_count = mt5.pcount(server, account, session)
if positions_count > 0:
    while positions_count > 0:
        positions_count = mt5.close_position(server, manager, password, account, session)
        time.sleep(0.5)