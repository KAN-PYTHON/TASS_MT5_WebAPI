#====================================================================================
# Библиотека функция для работы с MT5 WebAPI
#====================================================================================

def connect(server, manager, password):
    # Устанавливаем постоянно HTTPS соединение с MT5 WebAPI по менеджерскому логину
    # Возвращает requests.Session() или код ответа сервера status_code

    import requests
    import json
    import hashlib
    import secrets

    # Создаем сессию и отправляем первый запрос
    session = requests.Session()
    request_str = 'https://' + server + '/api/auth/start?version=3091&agent=WebAPI&login=' + manager + '&type=manager'
    request_result = session.get(request_str, verify=False)
    srv_rand = bytes.fromhex(request_result.json().get('srv_rand'))
    # Ответ сервера сохранен в srv_rand в виде байт кода 
    
    # Хэширование ответа серверу по правилам MT5
    password = password.encode('utf-16le')
    password = hashlib.md5(password).digest()
    password = hashlib.md5(password + b'WebAPI').digest()
    srv_rand = hashlib.md5(password+srv_rand).hexdigest()
    cli_rand = hashlib.md5(secrets.token_hex(16).encode('utf-16le')).hexdigest()
    # Ответ хэширован в srv_rand и cli_rand

    # Отправка ответа серверу MT5
    request_str = 'https://' + server + '/api/auth/answer?srv_rand_answer=' + srv_rand +'&cli_rand=' + cli_rand
    request_result = session.get(request_str, verify=False)

    if request_result.status_code == 200:
        return(session)
    else:
        return(request_result.status_code)
    
    # Конец функции
    # Пример: print(connect('webapi.educationvector.com', '1003', 'hf7jrf83er'))


def close_position(server, manager, password, account, session):
    # Закрываем первую в списке открытую позицию на счету account
    # Возвращает количество оставшихся открытых позиций

    import requests
    import json

    # Получаем данные всех открытых позиций
    request_result = session.get('https://' + server + '/api/position/get_page?login=' + account + '&offset=0&total=0')
    positions_count = len(request_result.json().get('answer'))
    if positions_count == 0:
        return(positions_count)

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
    
    # Запрашиваем список оставшихся открытых позиций
    request_result = session.get('https://' + server + '/api/position/get_page?login=' + account + '&offset=0&total=0')
    positions_count = len(request_result.json().get('answer'))
    
    return(positions_count)

    # Конец функции
    # Пример: print(close_position('webapi.educationvector.com', '1003', 'hf7jrf83er', '111511', session))


def pcount(server, account, session):
    # Возвращает количество открытых позиций

    import requests
    import json
    
    # Получаем данные всех открытых позиций
    request_result = session.get('https://' + server + '/api/position/get_page?login=' + account + '&offset=0&total=0')
    positions_count = len(request_result.json().get('answer'))

    return(positions_count)

    # Конец функции
    # Пример: print(pcount('webapi.educationvector.com', '111511', session))


def ord_count(server, account, session):
    # Возвращает количество отложенных ордеров

    import requests
    import json
    
    request_result = session.get('https://' + server + '/api/order/get_total?login=' + account + '&offset=0&total=0')
    orders_count = request_result.json().get('answer')['total']

    return(orders_count)

    # Конец функции
    # Пример: print(ordcount('webapi.educationvector.com', '111511', session))


def del_order(server, account, session):
    # Закрываем первую в списке открытую позицию на счету account
    # Возвращает количество оставшихся открытых позиций

    import requests
    import json

    # Получаем данные всех отложенных ордеров
    request_result = session.get('https://' + server + '/api/order/get_page?login=' + account + '&offset=0&total=0')
    orders_count = len(request_result.json().get('answer'))
    if orders_count == 0:
       return(orders_count)
    ticket = str(request_result.json().get('answer')[0]["Order"])

    # Отправляем запрос на удаление ордера
    request_result = session.post('https://' + server + '/api/order/delete?ticket=' + ticket)
    request_result = session.get('https://' + server + '/api/order/get_page?login=' + account + '&offset=0&total=0')
    orders_count = len(request_result.json().get('answer'))

    return(orders_count)

    # Конец функции
    # Пример: print(del_order('webapi.educationvector.com', '111511', session))


def mod_account_rights(server, account, session, rights):
    # Модификация прав счета
    # Параметр rights определяется как сумма прав IMTUser::EnUsersRights
    # 16743 - разрешено все кроме торговли
    # 16739 - разрешено все

    import requests
    import json

    rights = int(rights)
    request_str = 'https://' + server + '/api/user/get?login=' + account
    request_result = session.get(request_str, verify=False)

    request_str = 'https://' + server + '/api/user/update?login=' + account
    request_result = session.post(request_str, json={'Rights': rights})
    
    return(request_result.status_code)

    # Конец функции
    # Пример: print(mod_account_rights('webapi.educationvector.com', '111511', session, 16739))