import mt5_webapi_lib as mt5
import time
# Начальные установки подключения к MT5
server = 'webapi.educationvector.com'
manager = '1003'
password = 'hf7jrf83er'

# Получаем значение account из внешней DB
account = '111704'


def convert_to_eur(server, account, session):
    # Функция конвертирует Equity счета в заданную валюту

    # /api/user/get?login= - Свойства пользователя
    user_properties = session.get('https://' + server + '/api/user/get?login=' + account, verify=False)
    group_name = user_properties.json().get('answer')['Group']

    # /api/group/get?group= - Свойства группы
    group_properties = session.get(
        'https://' + server + '/api/group/get?group=' + group_name, verify=False)
    group_currency = group_properties.json().get('answer')['Currency']

    # /api/user/account/get?login= - Свойства счета
    account_properties = session.get('https://' + server + '/api/user/account/get?login=' + account, verify=False)
    account_equity = float(account_properties.json().get('answer')['Equity'])

    # Если валюты совпадают, возвращаем Equity
    if group_currency == 'EUR':
        return (account_equity)



    if group_currency == 'USD':
       currency_pair = 'EURUSD'
    elif group_currency == 'GBP':
        currency_pair = 'EURGBP'

    current_price = session.get('https://' + server + '/api/tick/last?symbol='+currency_pair+'&trans_id=0', verify=False)
    price = float(current_price.json().get('answer')[0]['Bid'])
    account_equity = account_equity * price
    return (account_equity)
    # Конец функции


session = mt5.connect(server, manager, password)
account_equity = convert_to_eur(server, account, session)
print('Equity =', account_equity+'EUR')



'''

if group_properties.json().get('answer')['Currency'] == 'USD':
    print()
'''
