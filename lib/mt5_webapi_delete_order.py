def ordcount(server, account, session):
    # Возвращает количество оставшихся открытых позиций

    import requests
    import json
    
    request_result = session.get('https://' + server + '/api/order/get_total?login=' + account + '&offset=0&total=0')
    orders_count = request_result.json().get('answer')['total']
    return(orders_count)

    # Конец функции
    # Пример: print(pcount('webapi.educationvector.com', '111511', session))




import requests
import json
import mt5_webapi_lib as mt5

server, manager, password, account= 'webapi.educationvector.com', '1003', 'hf7jrf83er', '111511'

# Получаем данные всех открытых позиций
session = mt5.connect(server, manager, password)
request_result = session.get('https://' + server + '/api/order/get_page?login=' + account + '&offset=0&total=0')
orders_count = len(request_result.json().get('answer'))
print("Открыто ордеров", orders_count)
if orders_count == 0:
    print("Выходим нах ...")
    exit()

ticket = str(request_result.json().get('answer')[0]["Order"])
# Отправляем запрос на закрытие позиции
request_str = 'https://' + server + '/api/order/delete?ticket=' + ticket
#request_result = session.post('https://' + server + '/api/order/delete?ticket=', json = {'ticket': ticket})
request_result = session.post('https://' + server + '/api/order/delete?ticket=' + ticket)
print(ticket)
print(request_str)