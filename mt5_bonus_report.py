import datetime
import pymysql


host = "89.108.65.107"
user = "mt5_tass_user"
password = "der#18DF$=12"
db_name = "mt5"

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
    file_name = 'txt\\bonus_report_' + datetime.datetime.now().strftime('%Y-%m-%d %H.%M') + '.html'
    with open(file_name, 'w') as file:
        file.write('<html>' + '\n')
        file.write('<head>'
                   '<meta http-equiv="content-type" content="text/html; charset=utf-8ru">'
                   '<style>'
                   '.table  {width: 800px; margin-bottom: 20px; border: 1px solid #dddddd; border-collapse: collapse;}'
                   '.table th {font-weight: bold; padding: 5px; background: #efefef; border: 1px solid #dddddd;}'
                   '.table td {border: 1px solid #dddddd; padding: 5px;}'
                   '</style>'
                   '<title>Bonus report</title>'
                   '</head>' + '\n')
        file.write('<body style = "font-family: Courier New">' + '\n')

        file.write('<div  style="margin: 10px">' + 'Bonus report at ' + str(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M')) + '</div>' + '\n')

        bonus_sum = "SELECT Login, SUM(Profit) as Sum FROM `mt5_deals_2022`" \
                    "WHERE Action NOT in (0, 1, 2)" \
                    "GROUP BY Login ORDER BY Login ASC"
        cursor.execute(bonus_sum)
        bonus_sum = cursor.fetchall()

        # deposit_sum = "SELECT Login, SUM(Profit) as Sum FROM `mt5_deals_2022`" \
        #             "WHERE Action in (0, 1, 2)" \
        #             "GROUP BY Login ORDER BY Login ASC"
        # cursor.execute(deposit_sum)
        # deposit_sum = cursor.fetchall()

        for result in bonus_sum:
            file.write('<table  class="table"' + '\n')
            file.write('<tr><th>Login</th><th>Deal</th><th>Profit</th><th>Comment</th></tr>' + '\n')

            bonus_all = "SELECT Deal, Time, Login, Action, Profit, Comment FROM `mt5_deals_2022`" \
                        "WHERE Action NOT in (0, 1, 2) and Login = " + str(result.get('Login'))
            cursor.execute(bonus_all)
            bonus_all = cursor.fetchall()

            for bonus in bonus_all:
                file.write('<tr>' + '\n')
                file.write('<td align="center">' + str(bonus.get('Login')) + '</td>' + '\n')
                file.write('<td align="center">' + str(bonus.get('Time')) + '</td>' + '\n')
                file.write('<td align="right">' + str(bonus.get('Profit')) + '</td>' + '\n')
                file.write('<td align="left">' + str(bonus.get('Comment')) + '</td>' + '\n')
                file.write('</tr>' + '\n')
            file.write('</table>' + '\n')
            file.write('<div  style="margin-bottom: 20px; width: 800px;" align = "right"> TOTAL: ' + str(
                result.get('Sum')) + ' USD</div>' + '\n')
        file.write('</body>' + '\n')
        file.write('</html>' + '\n')
    connection.close()

# MT5.send_report_email("anton.kurakin@gmail.com", file_name)
