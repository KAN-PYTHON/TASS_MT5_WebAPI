def pcount(server, account, session):
    # Возвращает количество оставшихся открытых позиций

    import requests
    import json
    
    request_result = session.get('https://' + server + '/api/position/get_page?login=' + account + '&offset=0&total=0')
    positions_count = len(request_result.json().get('answer'))
    return(positions_count)

    # Конец функции
    # Пример: print(pcount('webapi.educationvector.com', '111511', session))

import mt5_webapi_lib as mt5

server, manager, password, account= 'webapi.educationvector.com', '1003', 'hf7jrf83er', '111511'

# Получаем данные всех открытых позиций
session = mt5.connect(server, manager, password)
positions_count = pcount(server, account, session)
print("Осталось позиций:", positions_count)