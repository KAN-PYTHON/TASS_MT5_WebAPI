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


def sql_dials(group_filter, start, finish):
    result = "SELECT " \
                 "d.Login as Login, " \
                 "u.FirstName as Name, " \
                 "d.Time as Time, " \
                 "d.Action as Action, " \
                 "d.Profit as Profit, " \
                 "d.Comment as Comment " \
             "FROM mt5_deals_2022 d, mt5_users u " \
             "WHERE " \
                 "d.Action NOT in (0, 1, 2) and " \
                 "d.Time > " + start + " and " \
                 "d.Time < " + finish + " and " \
                 "d.Login = u.Login and " \
                 "LOCATE('" + group_filter + "', u.Group) > 0 "
    return result


'''=================================================================================================================='''
host = "89.108.65.107"
user = "mt5_tass_user"
password = "der#18DF$=12"
db_name = "mt5"
group_mask = ''
report_name = 'Bonus report'
start_date = datetime.datetime.now() + datetime.timedelta(days=-7)
start_date = "'"+start_date.strftime('%Y-%m-%d')+"'"
finish_date = datetime.datetime.now() + datetime.timedelta(days=1)
finish_date = "'"+finish_date.strftime('%Y-%m-%d')+"'"
'''=================================================================================================================='''
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

# Получаем данные из БД
with connection.cursor() as cursor:
    cursor.execute(sql_dials(group_mask, start_date, finish_date))
    dials = cursor.fetchall()

# Формируем шапку отчета
file_name = 'trade_report_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
with open(file_name, 'w') as f:
    f.write('<html>' + '\n')
    f.write('<head>'
            '<meta http-equiv="content-type" content="text/html; charset=utf-8ru">'
            '<style>'
            '.table  {width: 1200px; margin-bottom: 20px; border: 1px solid #dddddd; border-collapse: collapse;}'
            '.table th {font-weight: bold; padding: 5px; background: #efefef; border: 1px solid #dddddd;}'
            '.table td {border: 1px solid #dddddd; padding: 5px;}'
            '</style>'
            '<title>Trade report</title>'
            '</head>' + '\n')
    f.write('<body style = "font-family: Courier New">' + '\n')
    f.write('<div  style="margin: 10px">' + report_name + ' (' + group_mask+') from ' + start_date + ' to ' +
            finish_date + '</div>' + '\n')
    f.write('<table  class="table"' + '\n')
    f.write('<tr><th>Login</th><th>Name</th><th>Time</th><th>Profit</th><th>Comment</th>' + '\n')

    # Формируем тело таблицы
    for line in dials:
        f.write('<tr>' + '\n')
        f.write('<td align="center">' + str(line.get('Login')) + '</td>' + '\n')
        f.write('<td align="left">' + str(line.get('Name')) + '</td>' + '\n')
        f.write('<td align="center">' + str(line.get('Time')) + '</td>' + '\n')
        f.write('<td align="right">' + str(line.get('Profit')) + '</td>' + '\n')
        f.write('<td align="left">' + str(line.get('Comment')) + '</td>' + '\n')
        f.write('</tr>' + '\n')

    # Формируем подвал файла
    f.write('</table>' + '\n')
    f.write('</body>' + '\n')
    f.write('</html>' + '\n')

# Закрываем соединение с БД
connection.close()

# Отправляем email
send_email("anton.kurakin@gmail.com", file_name, report_name)
