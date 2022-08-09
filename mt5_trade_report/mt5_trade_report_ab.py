import time
import datetime
import pymysql


def send_email(receiver, filename, report_name):
    import os
    import datetime
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    # Подключение к почтовому серверу
    try:
        sender = "mt5.rport.sender@gmail.com"
        email_password = "dbqxujnizlnjiaae"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.ehlo()
        server.login(sender, email_password)
    except Exception as ex:
        return f"{ex}\nCheck your login or password please!"

    # Формируем тело письма и прикрепляем файл
    with open(filename) as f:
        file = f.read()
        message = MIMEMultipart()
        message["From"] = sender
        message["To"] = receiver
        message["Subject"] = report_name + ' ' + datetime.datetime.now().strftime('%Y-%m-%d')
        message.attach(MIMEText(file, "html"))
        attach_file = MIMEText(file)
        attach_file.add_header('content-disposition', 'attachment', filename=os.path.basename(filename))
        message.attach(attach_file)

    # Отправка email
    try:
        server.sendmail(sender, receiver, message.as_string())
    except Exception as ex:
        return f"{ex}\nSend email error!"


def sql_trades(group_filter, start, finish):
    result = "SELECT " \
                "d.Login as Login, " \
                "u.FirstName as Name, " \
                "ROUND(SUM(d.Storage),2) as Swaps, " \
                "ROUND(SUM(d.Commission),2) as Commission, " \
                "ROUND(SUM(d.Profit),2) as Profit, " \
                "ROUND(SUM(d.Storage)+SUM(d.Commission)+SUM(d.Profit), 2) as Total " \
             "FROM mt5_deals d, mt5_users u " \
             "WHERE " \
                "d.Action in (0, 1) and " \
                "d.Time > " + start + " and " \
                "d.Time < " + finish + " and " \
                "d.Login = u.Login and " \
                "LOCATE('" + group_filter + "', u.Group) > 0 " \
             "GROUP BY d.Login " \
             "ORDER BY d.Login"
    return result


def sql_trades_total(group_filter, start, finish):
    result = "SELECT " \
                "ROUND(SUM(d.Storage),2) as Swaps, " \
                "ROUND(SUM(d.Commission),2) as Commission, " \
                "ROUND(SUM(d.Profit),2) as Profit, " \
                "ROUND(SUM(d.Storage)+SUM(d.Commission)+SUM(d.Profit), 2) as Total " \
             "FROM mt5_deals d, mt5_users u " \
             "WHERE " \
                "d.Action in (0, 1) and " \
                "d.Time > " + start + " and " \
                "d.Time < " + finish + " and " \
                "d.Login = u.Login and " \
                "LOCATE('" + group_filter + "', u.Group) > 0 "
    return result


def main():
    # host = "89.108.65.107"
    # user = "mt5_tass_user"
    # password = "der#18DF$=12"
    # db_name = "mt5"
    host = "127.0.0.1"
    user = "nativeuser"
    password = "Cfvsqghjcnjqxtkjdtr1!"
    db_name = "test2"
    group_mask = 'abook'
    report_name = 'Trade report'
    start_date = datetime.datetime.now() + datetime.timedelta(days=-1000)
    start_date = "'"+start_date.strftime('%Y-%m-%d')+"'"
    finish_date = datetime.datetime.now() + datetime.timedelta(days=1)
    finish_date = "'"+finish_date.strftime('%Y-%m-%d')+"'"
    # Подключаемся к базе данных
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor)
    except Exception as _ex:
        print(f"{_ex}\nCheck your login or password please!")
        quit()
    # Формируем шапку отчета
    file_name = 'trade_report_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
    with open(file_name, 'w') as f:
        f.write('<html>' + '\n')
        f.write('<head>'
                '<meta http-equiv="content-type" content="text/html; charset=utf-8ru">'
                '<style>'
                '.table  {width: 800px; margin-bottom: 20px; border: 1px solid #dddddd; border-collapse: collapse;}'
                '.table th {font-weight: bold; padding: 5px; background: #efefef; border: 1px solid #dddddd;}'
                '.table td {border: 1px solid #dddddd; padding: 5px;}'
                '</style>'
                '<title>Trade report</title>'
                '</head>' + '\n')
        f.write('<body style = "font-family: Courier New">' + '\n')
        f.write('<div  style="margin: 10px">' + report_name + ' (' + group_mask + ') from ' + start_date + ' to ' +
                finish_date + '</div>' + '\n')
        f.write('<table  class="table"' + '\n')
        f.write('<tr><th>#</th><th>Login</th><th>Name</th><th>Swaps</th><th>Commission</th><th>Profit</th>'
                '<th>Total</th></tr>' + '\n')
        # Получаем детальные данные из БД и формируем тело таблицы
        with connection.cursor() as cursor:
            cursor.execute(sql_trades(group_mask, start_date, finish_date))
            trade_report = cursor.fetchall()
            i = 1
            for line in trade_report:
                f.write('<tr>' + '\n')
                f.write('<td align="right">' + str(i) + '</td>' + '\n')
                f.write('<td align="center">' + str(line.get('Login')) + '</td>' + '\n')
                f.write('<td align="left">' + str(line.get('Name')) + '</td>' + '\n')
                f.write('<td align="right">' + str(line.get('Swaps')) + '</td>' + '\n')
                f.write('<td align="right">' + str(line.get('Commission')) + '</td>' + '\n')
                f.write('<td align="right">' + str(line.get('Profit')) + '</td>' + '\n')
                f.write('<td align="right">' + str(line.get('Total')) + '</td>' + '\n')
                f.write('</tr>' + '\n')
                i += 1
            # Получаем суммарные данные из БД и формируем подвал файла
            cursor.execute(sql_trades_total(group_mask, start_date, finish_date))
            line = cursor.fetchall()
            f.write('<tr>' + '\n')
            f.write('<td align="right">' + str(i-1) + '</td>' + '\n')
            f.write('<td align="center">TOTAL:</td>' + '\n')
            f.write('<td align="center"> - * -</td>' + '\n')
            f.write('<td align="right">' + str(line[0]['Swaps']) + '</td>' + '\n')
            f.write('<td align="right">' + str(line[0]['Commission']) + '</td>' + '\n')
            f.write('<td align="right">' + str(line[0]['Profit']) + '</td>' + '\n')
            f.write('<td align="right">' + str(line[0]['Total']) + '</td>' + '\n')
            f.write('</tr>' + '\n')
            f.write('</table>' + '\n')
            f.write('</body>' + '\n')
            f.write('</html>' + '\n')
    # Закрываем соединение с БД
    connection.close()
    # Отправляем email
    # send_email("anton.kurakin@gmail.com", file_name, report_name)
    # send_email("info@tassfx.com", file_name, report_name)


'''=================================================================================================================='''
while True:
    if __name__ == "__main__":
        if datetime.datetime.now().strftime('%H:%M:%S') == '07:00:10':
            main()
            print("Trade report отправлен -", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            time.sleep(10)
