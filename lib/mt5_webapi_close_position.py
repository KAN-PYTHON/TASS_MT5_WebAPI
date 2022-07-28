import requests
import json
import mt5_webapi_lib as mt5

server, manager, password, account= 'webapi.educationvector.com', '1003', 'hf7jrf83er', '111511'

# Получаем данные всех открытых позиций
session = mt5.connect(server, manager, password)
request_result = session.get('https://' + server + '/api/position/get_page?login=' + account + '&offset=0&total=0')
positions_count = len(request_result.json().get('answer'))
print("Открыто позиций", positions_count)
if positions_count == 0:
    print("Выходим нах ...")
    exit()

# Выбираем тип операции BUY или SELL
if request_result.json().get('answer')[0]["Action"] == '0':
    type_position = '1'
else: type_position = '0'

# Отправляем запрос на закрытие позиции
request_result = session.post('https://' + server + '/api/dealer/send_request', 
                                json = {'Action': '200',
                                        'SourceLogin': manager,
                                        'Login': account,
                                        'Symbol': request_result.json().get('answer')[0]["Symbol"],
                                        'Volume': request_result.json().get('answer')[0]["Volume"],
                                        'Type': type_position, 
                                        'Position': request_result.json().get('answer')[0]["Position"]})

request_result = session.get('https://' + server + '/api/position/get_page?login=' + account + '&offset=0&total=0')
positions_count = len(request_result.json().get('answer'))
print("Осталось позиций:", positions_count)
