# encoding: utf-8
from api.helpers.service import Gis as gs
import json
import requests as req


def get_google(data):
    s = req.Session()
    key = "AIzaSyDMIfc6_9K7574xu18dG6ayTuAWsZtEOgE"
    url = """https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking
    &origins={}&destinations={}&key={}""".format(data[0], data[1], key)
    answer = s.get(url)
    answer = json.loads(answer.text)['rows'][0]['elements'][0]['duration']['text'].split()
    if len(answer) > 2:
        return int(answer[0])*60+int(answer[2])
    else:
        return int(answer[0])


def add_new_point(new_point):
    sql = " INSERT INTO Geo (Name, X, Y, Type, Descript, Rating, Time) VALUES (\'{}\', {}, {}, \'{}\', \'{}\', {}, {})".format(
        new_point["name"],
        float(new_point["x"]),
        float(new_point["y"]),
        new_point["type"],
        new_point["description"],
        int(new_point["rating"]),
        int(new_point["time"]))
    gs.SqlQuery(sql)

    sql = "SELECT id FROM Geo WHERE X={} AND Y={}".format(new_point["x"], new_point["y"])
    new_point["id"] = gs.SqlQuery(sql)
    new_point["id"] = int(new_point["id"][0]['id'])
    points = gs.SqlQuery("SELECT id, x, y FROM Geo WHERE id <> (SELECT last_value from geo_id_seq)")
    for i in range(len(points)):
        data = []
        disti = str(points[i]['x']) + "," + str(points[i]['y'])
        distj = str(new_point['x']) + "," + str(new_point['y'])
        data.append(disti)
        data.append(distj)
        answer = get_google(data)
        print(points[i]['id'], new_point['id'], answer)
        sql = "INSERT INTO geo_distance (point_1, point_2, distance) VALUES ({}, {}, {})".format(
            points[i]['id'],
            new_point['id'],
            answer)
        gs.SqlQuery(sql)

        gs.SqlQuery("INSERT INTO geo_distance (point_1, point_2, distance) VALUES ({}, {}, {})".format(
            new_point['id'],
            points[i]['id'],
            answer))
