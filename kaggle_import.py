import cx_Oracle
import csv

username = "PASHADB_KPI"
password = "17897AAS"
database = "localhost/xe"


# Підключення до бази даних
connection = cx_Oracle.connect(username, password, database)

cursor = connection.cursor()

# csv файл
filename = 'Video_Game_Sales_as_of_Jan_2017.csv'

with open(filename) as f:
    csv_reader = csv.DictReader(f)

    # Додамо то таблиці Region регіони продажів
    regions = ['NA', 'EU', 'JP', 'Other']
    regions_insert_query_template = "INSERT INTO REGION VALUES (:region)"

    for region in regions:
        cursor.execute(regions_insert_query_template, region = region)

    connection.commit()

    game_names = []
    publishers = []
    platforms = []
    genres = []
    year_of_release = []
    na_sales = []
    eu_sales = []
    jp_sales = []
    other_sales = []

    # Додаємо дані до таблиці Game, Genre, Publisher, Platform
    for dict_row in csv_reader:
        game_names.append(dict_row['Name'])
        publishers.append(dict_row['Publisher'])
        platforms.append(dict_row['Platform'])
        genres.append(dict_row['Genre'])

        year_of_release.append(dict_row['Year_of_Release'])

        na_sales.append(dict_row['NA_Sales'])
        eu_sales.append(dict_row['EU_Sales'])
        jp_sales.append(dict_row['JP_Sales'])
        other_sales.append(dict_row['Other_Sales'])

    game_names_unique = list(set(game_names))
    publishers_unique = list(set(publishers))
    platforms_unique = list(set(platforms))
    genres_unique = list(set(genres))

    game_query_template = "INSERT INTO GAME VALUES (:game_name)"
    publisher_query_template = "INSERT INTO PUBLISHER VALUES (:publisher)"
    platform_query_template = "INSERT INTO PLATFORM VALUES (:platform)"
    genre_query_template = "INSERT INTO GENRE VALUES (:genre)"

    cursor.prepare(game_query_template)
    cursor.executemany(None, list(map(lambda x: [x], game_names_unique)))
    
    cursor.prepare(publisher_query_template)
    cursor.executemany(None, list(map(lambda x: [x], publishers_unique)))

    cursor.prepare(platform_query_template)
    cursor.executemany(None, list(map(lambda x: [x], platforms_unique)))

    cursor.prepare(genre_query_template)
    cursor.executemany(None, list(map(lambda x: [x], genres_unique)))

    connection.commit()

    # Додаємо дані до таблиці GameGenre
    gameGenre_query_template = "INSERT INTO GAMEGENRE VALUES (:name, :genre)"

    cursor.prepare(gameGenre_query_template)
    cursor.executemany(None, list(map(lambda name: [name, genres[game_names.index(name)]], game_names_unique)))

    connection.commit()

    # Додаємо дані до таблиці GamePlatformPublisher та GameYear
    gamePlatformPublisher_query_template = "INSERT INTO GAMEPLATFORMPUBLISHER VALUES (:name, :platform, :publisher)"
    gameYear_query_template = "INSERT INTO GAMEYEAR VALUES (:name, :platform, :publisher, :year)"

    for idx in range(0, len(game_names)):
        try:
            cursor.execute(gamePlatformPublisher_query_template, name = game_names[idx], platform = platforms[idx],
                           publisher = publishers[idx])
            cursor.execute(gameYear_query_template, name = game_names[idx], platform = platforms[idx],
                           publisher = publishers[idx], year = year_of_release[idx])
        except:
            pass

    connection.commit()

    gameSales_query_template = "INSERT INTO GAMESALES VALUES (:name, :platform, :publisher, :region, :sales)"

    # Додаємо дані до таблиці GameSales
    for idx in range(0, len(game_names)):
       
        try:
            cursor.execute(gameSales_query_template, name = game_names[idx], platform = platforms[idx],
                           publisher = publishers[idx], region = 'EU', sales = float(eu_sales[idx]))
            cursor.execute(gameSales_query_template, name = game_names[idx], platform = platforms[idx],
                           publisher = publishers[idx], region = 'JP', sales = float(jp_sales[idx]))
            cursor.execute(gameSales_query_template, name = game_names[idx], platform = platforms[idx],
                           publisher = publishers[idx], region = 'Other', sales = float(other_sales[idx]))
            cursor.execute(gameSales_query_template, name = game_names[idx], platform = platforms[idx],
                           publisher = publishers[idx], region = 'NA', sales = float(na_sales[idx]))
        except cx_Oracle.IntegrityError:
            print('Цей запис вже існує')
            continue

    connection.commit()


cursor.close()
connection.close()
