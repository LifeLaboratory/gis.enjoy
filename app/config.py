HEADER = {'Access-Control-Allow-Origin': '*'}
DATABASE = {
    "dbname": "life_game_service",
    "user": "life_dev",
    "host": "90.189.132.25",
    "password": "PINLOX!@#"
}
"""
INDEXES = {"Парк": 0,
           "Памятник": 1,
           "Музей": 2,
           "Театр": 3,
           "Галерея": 4,
           "Фонтан": 5,
           "Разное": 6,
           "парк": 0,
           "памятник": 1,
           "музей": 2,
           "театр": 3,
           "галерея": 4,
           "фонтан": 5,
           "разное": 6,
           "площадь": 7,
           "пешеходная":8,
           "цирк": 9,
           "разное, небоскрёб": 10,
           "храм": 11
           }
"""
"""
INDEXES ={}
sql = "SELECT distinct type FROM Geo"
result = SqlQuery(sql)
for i in range(len(result)):
    #print(i, [result[i]['type']])
    INDEXES[result[i]['type']] = i
print(INDEXES)
"""