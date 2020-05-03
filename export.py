# export.py імпортує дані з кожної таблиці в окремий csv

import cx_Oracle
import csv

# Пароль password прибрано в цілях безпеки
username = "PASHADB_KPI"
password = ""
database = "localhost/xe"

# Підключення до бази даних
connection = cx_Oracle.connect(username, password, database)
cursor = connection.cursor()

# Назви усіх таблиць
table_names = ['GAME', 'GENRE', 'PUBLISHER', 'PLATFORM', 'REGION', 'GAMEGENRE', 'GAMEPLATFORMPUBLISHER', 'GAMEYEAR', 'GAMESALES']

# Проходимося по всім таблицям зі списку
for table_name in table_names:

    # Створюємо і відкриваємо відповідні файли
    with open("{}.csv".format(table_name), 'w', newline="") as f:
        all_data_query_template = "SELECT * FROM {}".format(table_name)

        # Отримаємо дані з таблиці
        cursor.execute(all_data_query_template)

        # Отримаємо заголовки з таблиці
        header_col_titles = list(map(lambda header: header[0], cursor.description))

        csv_write = csv.writer(f, delimiter = ',')

        # Запишемо назви стовпчиків та запишемо дані з таблиць
        csv_write.writerow(header_col_titles)

        for row_result in cursor:
            csv_write.writerow(row_result)

cursor.close()
connection.close()
