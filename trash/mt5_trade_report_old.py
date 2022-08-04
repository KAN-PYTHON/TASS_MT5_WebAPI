import datetime
import pymysql
from lib import mt5_webapi_lib as MT5


def sql_trades(group_filter, start):
    result = "SELECT " \
                "d.Login as Login, " \
                "u.FirstName as Name, " \
                "ROUND(SUM(d.Storage),2) as Swaps, " \
                "ROUND(SUM(d.Commission),2) as Commission, " \
                "ROUND(SUM(d.Profit),2) as Profit, " \
                "ROUND(SUM(d.Storage)+SUM(d.Commission)+SUM(d.Profit), 2) as Total " \
             "FROM mt5_deals_2022 d, mt5_users u " \
             "WHERE d.Action in (0, 1) and " \
                "d.Time > " + start + " and " \
                "d.Login = u.Login and " \
                "LOCATE('" + group_filter + "', u.Group) > 0 " \
             "GROUP BY d.Login " \
             "ORDER BY d.Login"
    return result


def sql_trades_total(group_filter, start):
    result = "SELECT " \
                "ROUND(SUM(d.Storage),2) as Swaps, " \
                "ROUND(SUM(d.Commission),2) as Commission, " \
                "ROUND(SUM(d.Profit),2) as Profit, " \
                "ROUND(SUM(d.Storage)+SUM(d.Commission)+SUM(d.Profit), 2) as Total " \
             "FROM mt5_deals_2022 d, mt5_users u " \
             "WHERE d.Action in (0, 1) and " \
                "d.Time > " + start + " and " \
                "d.Login = u.Login and " \
                "LOCATE('" + group_filter + "', u.Group) > 0 "
    return result


host = "89.108.65.107"
user = "mt5_tass_user"
password = "der#18DF$=12"
db_name = "mt5"
group_mask = 'bbook'
start_date = "'2022-01-01 00:00:00'"

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

with connection.cursor() as cursor:
    file_name = 'txt\\trade_report_' + datetime.datetime.now().strftime('%Y-%m-%d') + '.html'
    with open(file_name, 'w') as file:
        file.write('<html>' + '\n')
        file.write('<head>'
                   '<meta http-equiv="content-type" content="text/html; charset=utf-8ru">'
                   '<style>'
                   '.table  {width: 800px; margin-bottom: 20px; border: 1px solid #dddddd; border-collapse: collapse;}'
                   '.table th {font-weight: bold; padding: 5px; background: #efefef; border: 1px solid #dddddd;}'
                   '.table td {border: 1px solid #dddddd; padding: 5px;}'
                   '</style>'
                   '<title>Trade report</title>'
                   '</head>' + '\n')
        file.write('<body style = "font-family: Courier New">' + '\n')
        file.write('<div  style="margin: 10px">' + 'Trade report (' + group_mask+') from ' + start_date + ' to ' + str(
            datetime.datetime.now().strftime('%Y-%m-%d')) + '</div>' + '\n')
        file.write('<table  class="table"' + '\n')
        file.write('<tr><th>#</th><th>Login</th><th>Name</th><th>Swaps</th><th>Commission</th><th>Profit</th>'
                   '<th>Total</th></tr>' + '\n')
        cursor.execute(sql_trades(group_mask, start_date))
        trade_report = cursor.fetchall()
        i = 1
        for line in trade_report:
            file.write('<tr>' + '\n')
            file.write('<td align="right">' + str(i) + '</td>' + '\n')
            file.write('<td align="center">' + str(line.get('Login')) + '</td>' + '\n')
            file.write('<td align="left">' + str(line.get('Name')) + '</td>' + '\n')
            file.write('<td align="right">' + str(line.get('Swaps')) + '</td>' + '\n')
            file.write('<td align="right">' + str(line.get('Commission')) + '</td>' + '\n')
            file.write('<td align="right">' + str(line.get('Profit')) + '</td>' + '\n')
            file.write('<td align="right">' + str(line.get('Total')) + '</td>' + '\n')
            file.write('</tr>' + '\n')
            i += 1
        cursor.execute(sql_trades_total(group_mask, start_date))
        line = cursor.fetchall()
        file.write('<tr>' + '\n')
        file.write('<td align="right">' + str(i-1) + '</td>' + '\n')
        file.write('<td align="center">TOTAL:</td>' + '\n')
        file.write('<td align="center"> - * -</td>' + '\n')
        file.write('<td align="right">' + str(line[0]['Swaps']) + '</td>' + '\n')
        file.write('<td align="right">' + str(line[0]['Commission']) + '</td>' + '\n')
        file.write('<td align="right">' + str(line[0]['Profit']) + '</td>' + '\n')
        file.write('<td align="right">' + str(line[0]['Total']) + '</td>' + '\n')
        file.write('</tr>' + '\n')
        file.write('</table>' + '\n')
        file.write('</body>' + '\n')
        file.write('</html>' + '\n')
connection.close()

# MT5.send_report_email("anton.kurakin@gmail.com", file_name)
