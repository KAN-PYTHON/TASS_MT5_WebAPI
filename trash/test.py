import datetime
print('133033991460252848', datetime.datetime.fromtimestamp(133033991460252848))
# 1540289822.637441
# 133033991460252848
print(datetime.datetime.strftime(133033991460252848)
# select_all_rows = "SELECT * FROM `users`"
# SELECT
# Deal, Login, Action, Profit, Comment
# FROM
# mt5_deals_2022
# WHERE Login = 9999 and Action NOT in (0, 1)


# cursor.execute("SELECT * FROM `users`")
# print('rows', type(rows), rows)
# print('========================')
# print('rows[0]', type(rows[0]), rows[0])
# print('========================')
# print('rows[0].items()', type(rows[0].items()), rows[0].items())
# print('========================')
# print('rows[0].keys()', type(rows[0].keys()), rows[0].keys())
# print('========================')
# print('rows[0].get()', type(rows[0].get('Deal')), rows[0].get('Deal'))
# print('========================')
# print('rows[0].values()', type(rows[0].values()), rows[0].values())
# print('========================')
# print("rows[3].get('Deal'))", type(rows[0].get('Deal')), rows[0].get('Deal'))
# print('========================')

# file.write('<html>' + '\n')
# file.write('<head><title> Отчет по буносам</title></head>' + '\n')
# file.write('<body>' + '\n')
# file.write('<table border = "1">' + '\n')
# file.write('<tr>' + '\n')
# file.write('<td>' + 'Привет!' + '</td>' + '\n')
# file.write('</tr>' + '\n')
# file.write('</table>' + '\n')
# file.write('</body>' + '\n')
# file.write('</html>' + '\n')

# cursor = connection.cursor()

# create table
# with connection.cursor() as cursor:
#     create_table_query = "CREATE TABLE `users`(id int AUTO_INCREMENT," \
#                          " name varchar(32)," \
#                          " password varchar(32)," \
#                          " email varchar(32), PRIMARY KEY (id));"
#     cursor.execute(create_table_query)
#     print("Table created successfully")

# insert data
# with connection.cursor() as cursor:
#     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Anna', 'qwerty', 'anna@gmail.com');"
#     cursor.execute(insert_query)
#     connection.commit()

# with connection.cursor() as cursor:
#     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Victor', '123456', 'victor@gmail.com');"
#     cursor.execute(insert_query)
#     connection.commit()
#
# with connection.cursor() as cursor:
#     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Oleg', '112233', 'olegan@mail.ru');"
#     cursor.execute(insert_query)
#     connection.commit()

# with connection.cursor() as cursor:
#     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Oleg', 'kjlsdhfjsd', 'ole2gan@mail.ru');"
#     cursor.execute(insert_query)
#     connection.commit()
#
# with connection.cursor() as cursor:
#     insert_query = "INSERT INTO `users` (name, password, email) VALUES ('Oleg', '889922', 'olegan3@mail.ru');"
#     cursor.execute(insert_query)
#     connection.commit()

# update data
# with connection.cursor() as cursor:
#     update_query = "UPDATE `users` SET password = 'xxxXXX' WHERE name = 'Oleg';"
#     cursor.execute(update_query)
#     connection.commit()

# delete data
# with connection.cursor() as cursor:
#     delete_query = "DELETE FROM `users` WHERE id = 5;"
#     cursor.execute(delete_query)
#     connection.commit()

# drop table
# with connection.cursor() as cursor:
#     drop_table_query = "DROP TABLE `users`;"
#     cursor.execute(drop_table_query)
