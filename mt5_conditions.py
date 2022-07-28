"""
Скрипт сравнивает торговые условия двух счетов MT5
"""
import time
import MetaTrader5 as MT5

MASTER_SERVER = "TASS-Live"
MASTER_LOGIN = 1669
MASTER_PASSWORD = "qwe123456"

SLAVE_SERVER = "CFITrader-Demo"
SLAVE_LOGIN = 31672457
SLAVE_PASSWORD = "qwe123456"


def mt5_symbols_info_get(server, login, password):
    # Функция возвращает информацию о всех символах.
    # Активируем торговый терминал MT5
    while not MT5.initialize():
        time.sleep(5)
        print("MT5 Initialize failed, error code =", MT5.last_error())
    # Подключаемся к торговому счету и получаем данные по всем символам
    while not MT5.login(login=login, server=server, password=password, timeout=20000):
        time.sleep(5)
        print("MT5 "+str(login) + " login failed, error code =", MT5.last_error())
    result = MT5.symbols_get()
    # Добавляем все символы в Market Watch
    for s in result:
        MT5.symbol_select(s.name, True)

    # Записываем в файл данные символов MASTER
    with open('txt\_symbols_' + str(login) + '.txt', "w+") as f:
        i = 0
        while i < len(result):
            f_str = [result[i].name,
                     result[i].digits,
                     result[i].spread,
                     round(result[i].swap_long, 2),
                     round(result[i].swap_short, 2)]
            f.write(str(f_str) + "\n")
            i += 1

    return result


'''=================================================================================================================='''
master = mt5_symbols_info_get(MASTER_SERVER, MASTER_LOGIN, MASTER_PASSWORD)
print('Всего символов MASTER:', len(master))
slave = mt5_symbols_info_get(SLAVE_SERVER, SLAVE_LOGIN, SLAVE_PASSWORD)
print('Всего символов SLAVE:', len(slave))

# Записываем в файл сравнительные данные MASTER и SLAVE
with open('txt\_symbols_' + SLAVE_SERVER + '.txt', "w+") as f:
    i = 0
    f.write(SLAVE_SERVER + '\n')
    f.write('Name / Spread / Swap long / Swap short / Swap Mode' + '\n' + '\n')
    while i < len(master):
        j = 0
        while j < len(slave):
            if master[i].name in slave[j].name:
                if (master[i].digits - slave[j].digits) > 0:
                    delta = 10**(master[i].digits - slave[j].digits)
                elif (master[i].digits - slave[j].digits) < 0:
                    delta = 1 / 10**(slave[j].digits - master[i].digits)
                else:
                    delta = 1

                if master[i].swap_mode == slave[j].swap_mode:
                    master_swap_long = round(master[i].swap_long, 2)
                    master_swap_short = round(master[i].swap_short, 2)
                    slave_swap_long = round(slave[j].swap_long * delta, 2)
                    slave_swap_short = round(slave[j].swap_short * delta, 2)
                else:
                    if master[i].swap_mode == 0:
                        master_swap_long = 0
                        master_swap_short = 0
                    else:
                        master_swap_long = round(master[i].swap_long, 2)
                        master_swap_short = round(master[i].swap_short, 2)
                    slave_swap_long = round(slave[j].swap_long, 2)
                    slave_swap_short = round(slave[j].swap_short, 2)
                f_str = [
                        master[i].name, slave[j].name,
                        master[i].spread, round(slave[j].spread * delta, 2),
                        master_swap_long, slave_swap_long,
                        master_swap_short, slave_swap_short,
                        master[i].swap_mode, slave[j].swap_mode
                        ]
                f.write(str(f_str) + "\n")
                print(str(f_str))
            j += 1
        i += 1

# MT5.shutdown()
