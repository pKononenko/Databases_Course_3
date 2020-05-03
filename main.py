import cx_Oracle

import re

import plotly.graph_objects as go

import chart_studio
import chart_studio.plotly as py
import chart_studio.dashboard_objs as dashboard


def fileId_from_url(url):
    raw_fileId = re.findall("~[A-z.]+/[0-9]+", url)[0][1: ]
    return raw_fileId.replace('/', ':')


# Підключення до chart-studio аккаунту
# api key прибрано в цілях безпеки
chart_studio.tools.set_credentials_file(username='pavlo.kononenko', api_key='')

username = "PASHADB_KPI"
password = "17897AAS"
database = "localhost/xe"

# Підключення до бази даних
connection = cx_Oracle.connect(username, password, database)

# View Запит 1 - Вивести назву гри та кількість її продажів на усіх платформах
query_sales = \
"""
    SELECT 
        game_name, 
        SUM(REGION_SALES) AS TOTAL_SALES
    FROM GAMEDATA
    GROUP BY game_name
    ORDER BY TOTAL_SALES DESC
"""

game_names = []
total_sales = []


# View Запит 2 - Вивести жанр та відсоток цього жанру на ринку
query_percentage = \
"""
    SELECT
        genre,
        round( count(DISTINCT game_name) * 100 / ( SELECT count(*) FROM (SELECT DISTINCT GAME_NAME FROM GAMEDATA) ) , 2) AS PERCENTAGE
    FROM GAMEDATA
    GROUP BY genre
    ORDER BY PERCENTAGE DESC
"""

genres = []
percentages = []


# View Запит 3 - Вивести динаміку кількості ігр, випущених кожного року
query_dynamic = \
"""
    SElECT 
        year_of_release,
        COUNT(game_name)/COUNT(DISTINCT region) AS GAMES_COUNT
    FROM GAMEDATA
    GROUP BY year_of_release
    ORDER BY year_of_release
"""

years = []
games_count = []


cursor = connection.cursor()
cursor.execute(query_sales)

# Рузультати першого запиту (список множин)
result_sales = cursor.fetchall()

# Додавання данних з першого запиту
for row in result_sales[0:1000]:
    game_names.append(row[0])
    total_sales.append(row[1])

# Побудова стовбчикової діаграми
bar_data = \
[
    go.Bar
    (
        x = game_names,
        y = total_sales,
        text = total_sales,
        textposition = 'auto'
    )
]

# Стиль макету
bar_layout = go.Layout(
    title = "Ігри та їх продажі",

    xaxis = dict(
        title='Ігри',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),

    yaxis = dict(
        title='Продажі (в мільйонах)',
        rangemode='nonnegative',
        autorange=True,
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)

fig = go.Figure(data = bar_data, layout = bar_layout)
games_total_sales_bar = py.plot(fig, filename = 'games_total_sales_bar_view')


cursor.execute(query_percentage)

# Рузультати другого запиту
result_percentage = cursor.fetchall()

# Додавання данних з дпугого запиту
for row in result_percentage:
    genres.append(row[0])
    percentages.append(row[1])

# Побудова кругової діаграми
pie_data = go.Pie(
    labels = genres,
    values = percentages,
    title = "Відсоток кожного жанру на ринку"
)
genres_percentages_pie = py.plot([pie_data], filename = 'genres_percentages_pie_view')


cursor.execute(query_dynamic)

# Додавання результатів третього запиту
result_dynamic = cursor.fetchall()

for row in result_dynamic:
    years.append(row[0])
    games_count.append(row[1])

# Побудова графіка
scatter_data = [go.Scatter(
    x = years,
    y = games_count,
)]

layout_scatter = go.Layout(
    title="Динаміка кількості ігор кожного року",

    xaxis=dict(
        title="Роки",
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    ),

    yaxis=dict(
        title='Кількість випущених ігор',
        titlefont=dict(
            family='Courier New, monospace',
            size=18,
            color='#7f7f7f'
        )
    )
)
scatter_plot = go.Figure(data = scatter_data, layout = layout_scatter)
games_years_dynamic_scatter = py.plot(scatter_plot, filename = "games_years_dynamic_scatter_view")


# Закрити підключення
cursor.close()
connection.close()


# Створення dashboard
lab_db_dashboard = dashboard.Dashboard()

games_total_sales_bar_id = fileId_from_url(games_total_sales_bar)
genres_percentages_pie_id = fileId_from_url(genres_percentages_pie)
games_years_dynamic_scatter_id = fileId_from_url(games_years_dynamic_scatter)

box_1= {
    'type': 'box',
    'boxType': 'plot',
    'fileId': games_total_sales_bar_id,
    'title': 'Ігри та їх продажі (view запит 1)'
}

box_2 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': genres_percentages_pie_id,
    'title': 'Відсоток кожного жанру на ринку (view запит 2)'
}

box_3 = {
    'type': 'box',
    'boxType': 'plot',
    'fileId': games_years_dynamic_scatter_id,
    'title': 'Динаміка кількості ігор, які випускаються кожного року (view запит 3)'
}

lab_db_dashboard.insert(box_3)
lab_db_dashboard.insert(box_2, 'below', 1)
lab_db_dashboard.insert(box_1, 'left', 2)

py.dashboard_ops.upload(lab_db_dashboard, 'Games_VIEW_version')
