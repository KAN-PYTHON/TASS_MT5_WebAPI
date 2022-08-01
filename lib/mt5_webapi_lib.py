"""
====================================================================================
 Библиотека функция для работы с MT5 WebAPI
====================================================================================
"""


def connect(server, manager, password):
    # Устанавливаем постоянно HTTPS соединение с MT5 WebAPI по менеджерскому логину
    # Возвращает requests.Session() или код ответа сервера status_code

    import requests
    import hashlib
    import secrets

    # Создаем сессию и отправляем первый запрос
    session = requests.Session()
    request_str = 'https://' + server + '/api/auth/start?version=3091&agent=WebAPI&login=' + manager + '&type=manager'
    request_result = session.get(request_str, verify=False)
    srv_rand = bytes.fromhex(request_result.json().get('srv_rand'))
    # Ответ сервера сохранен в srv_rand в виде байт-кода

    # Хеширование ответа серверу по правилам MT5
    password = password.encode('utf-16le')
    password = hashlib.md5(password).digest()
    password = hashlib.md5(password + b'WebAPI').digest()
    srv_rand = hashlib.md5(password + srv_rand).hexdigest()
    cli_rand = hashlib.md5(secrets.token_hex(16).encode('utf-16le')).hexdigest()
    # Ответ хэширован в srv_rand и cli_rand

    # Отправка ответа серверу MT5
    request_str = 'https://' + server + '/api/auth/answer?srv_rand_answer=' + srv_rand + '&cli_rand=' + cli_rand
    request_result = session.get(request_str, verify=False)

    if request_result.status_code == 200:
        return session
    else:
        return request_result.status_code

    # Конец функции
    # Пример: print(connect('webapi.rrr.com', '1003', 'hf7jrf83er'))


def close_position(server, manager, account, session):
    # Закрываем первую в списке открытую позицию на счету account
    # Возвращает количество оставшихся открытых позиций

    # Получаем данные всех открытых позиций
    request_result = session.get('https://' + server + '/api/position/get_page?login=' + account + '&offset=0&total=0')
    positions_count = len(request_result.json().get('answer'))
    if positions_count == 0:
        return positions_count

    # Выбираем тип операции BUY или SELL
    if request_result.json().get('answer')[0]["Action"] == '0':
        type_position = '1'
    else:
        type_position = '0'

    # Отправляем запрос на закрытие позиции
    session.post('https://' + server + '/api/dealer/send_request',
                 json={'Action': '200',
                       'SourceLogin': manager, 'Login': account,
                       'Symbol': request_result.json().get('answer')[0]["Symbol"],
                       'Volume': request_result.json().get('answer')[0]["Volume"],
                       'Type': type_position,
                       'Position': request_result.json().get('answer')[0]["Position"]})

    # Запрашиваем список оставшихся открытых позиций
    request_result = session.get('https://' + server + '/api/position/get_page?login=' + account + '&offset=0&total=0')
    positions_count = len(request_result.json().get('answer'))

    return positions_count

    # Конец функции
    # Пример: print(close_position('webapi.rrr.com', '1003', 'hf7jrf83er', '111511', session))


def position_count(server, account, session):
    # Возвращает количество открытых позиций

    # Получаем данные всех открытых позиций
    request_result = session.get('https://' + server + '/api/position/get_page?login=' + account + '&offset=0&total=0')
    positions_count = len(request_result.json().get('answer'))

    return positions_count

    # Конец функции
    # Пример: print(position_count('webapi.rrr.com', '111511', session))


def order_count(server, account, session):
    # Возвращает количество отложенных ордеров

    request_result = session.get('https://' + server + '/api/order/get_total?login=' + account + '&offset=0&total=0')
    count = request_result.json().get('answer')['total']

    return count

    # Конец функции
    # Пример: print(order_count('webapi.rrr.com', '111511', session))


def del_order(server, account, session):
    # Закрываем первую в списке открытую позицию на счету account
    # Возвращает количество оставшихся открытых позиций

    # Получаем данные всех отложенных ордеров
    request_result = session.get('https://' + server + '/api/order/get_page?login=' + account + '&offset=0&total=0')
    orders_count = len(request_result.json().get('answer'))
    if orders_count == 0:
        return orders_count
    ticket = str(request_result.json().get('answer')[0]["Order"])

    # Отправляем запрос на удаление ордера
    session.post('https://' + server + '/api/order/delete?ticket=' + ticket)
    request_result = session.get('https://' + server + '/api/order/get_page?login=' + account + '&offset=0&total=0')
    orders_count = len(request_result.json().get('answer'))

    return orders_count

    # Конец функции
    # Пример: print(del_order('webapi.rrr.com', '111511', session))


def mod_account_rights(server, account, session, rights):
    # Модификация прав счета
    # Параметр rights определяется как сумма прав IMTUser::EnUsersRights
    # 16743 - разрешено все кроме торговли
    # 16739 - разрешено все

    rights = int(rights)
    request_str = 'https://' + server + '/api/user/get?login=' + account
    session.get(request_str, verify=False)

    request_str = 'https://' + server + '/api/user/update?login=' + account
    request_result = session.post(request_str, json={'Rights': rights})

    return request_result.status_code


# Конец функции
# Пример: print(mod_account_rights('webapi.rrr.com', '111511', session, 16739))


def send_email_txt(receiver, subject, message):
    import smtplib
    from email.mime.text import MIMEText
    sender = "mt5.tassfx@gmail.com"
    password = "axyvxpilslxzvwrh"
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.ehlo()
    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = subject
        server.sendmail(sender, receiver, msg.as_string())
    except Exception as _ex:
        return _ex
    return 0
# Конец функции
# # Пример: print(send_email_txt('anton.kurakin@gmail.com', 'Тебе письмо', 'Привет брат!')))


def send_report_email(receiver, file_name):
    import os
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    try:
        sender = "mt5.rport.sender@gmail.com"
        password = "dbqxujnizlnjiaae"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.ehlo()
        server.login(sender, password)
    except Exception as _ex:
        return f"{_ex}\nCheck your login or password please!"

    with open(file_name) as file:
        report_file = file.read()

    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = "Bonus report - " + os.path.basename(file_name)
    message.attach(MIMEText(report_file, "html"))

    with open(file_name) as file:
        report_file = MIMEText(file.read())

    report_file.add_header('content-disposition', 'attachment', filename=os.path.basename(file_name))
    message.attach(report_file)

    try:
        server.sendmail(sender, receiver, message.as_string())
    except Exception as _ex:
        return f"{_ex}\nSend email error!"
# Конец функции
# Пример: send_report_email("anton.kurakin@gmail.com", "requirements.txt")
