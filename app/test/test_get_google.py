__author__ = 'RaldenProg'


import json
from app.api.get_google_dist import get_google, get_coords
from pprint import pprint
from app.data.get_and_parse_data import db_connect
from api.sql import SqlQuery
#print(get_google(["54.9870301969,82.8739339379", "55.0666090889,82.9952098502"]))

#touch = ((54.9870301969, 82.8739339379), (55.0666090889, 82.9952098502))
#print(get_coords(touch, 500))

def add_new_point(new_point):
    points = SqlQuery("SELECT id, x, y FROM Geo WHERE id <> currval('geo_id_seq')")
    for i in range(len(points)):
        data = []
        disti = str(points[i]['x']) + "," + str(points[i]['y'])
        distj = str(new_point['x']) + "," + str(new_point['y'])
        data.append(disti)
        data.append(distj)
        answer = get_google(data)
        print(points[i]['id'], new_point['id'], answer)

        SqlQuery("INSERT INTO geo_distance" \
                  " VALUES (null, {}, {}, {})".format(
                points[i]['id'],
                new_point['id'],
                answer))
        SqlQuery("INSERT INTO geo_distance" \
                 " VALUES (null, {}, {}, {})".format(
            new_point['id'],
            points[i]['id'],
            answer))


def get():
    sql = "SELECT id, x, y FROM Geo"
    connect, current_connect = db_connect()
    current_connect.execute(sql)
    result = current_connect.fetchall()
    return result


def generate_distance():
    connect, current_connect = db_connect()
    result = get()
    data = []
    for i in range(len(result)):
        for j in range(i+1, len(result)):
            data = []
            disti = str(result[i]['x'])+","+str(result[i]['y'])
            distj = str(result[j]['x'])+","+str(result[j]['y'])
            data.append(disti)
            data.append(distj)
            answer = get_google(data)
            print(result[i]['id'], result[j]['id'], answer)

            sql = "INSERT INTO geo_distance" \
                  " VALUES (null, {}, {}, {})".format(
                result[i]['id'],
                result[j]['id'],
                answer)
            print(sql)
            try:
                current_connect.execute(sql)
                connect.commit()
            except:
                print('error: Ошибка запроса к базе данных.')

generate_distance()
