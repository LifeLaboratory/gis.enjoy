# encoding: utf-8
from api.helpers.service import Gis as gs
import json
import requests as req
from api.database.from_google import get_from_google
import logging

logging.basicConfig(filename='logger.log',
                        format='%(filename)-12s[LINE:%(lineno)d] %(levelname)-8s %(message)s %(asctime)s ',
                        level=logging.DEBUG)

TYPES = ['Парки', 'Парк', 'Сады', 'Фонтаны', 'Достопримечательности', "Монументы", 'памятники+культуры', 'красивые+места',
         'кинотеатры', 'Природные+достопримечательности', 'храмы', 'церкви', 'театры', 'опера', 'стадионы', 'мемориалы',
         'зоопарки', 'балет', 'собор', 'галерея', 'выставка', 'сквер', 'аквапарк', 'капелла', 'цирк']

def get_google(data):
    s = req.Session()
    key = "AIzaSyDdrExQrPV2n8Y58q7EYwVgGog-6ph9LB8"
    url = """https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking
    &origins={}&destinations={}&key={}""".format(data[0], data[1], key)
    #print(url)
    answer = s.get(url)
    answer = json.loads(answer.text)['rows'][0]['elements'][0]['duration']['text'].split()
    if len(answer) > 2:
        return int(answer[0])*60+int(answer[2])
    else:
        return int(answer[0])


def add_new_point(new_point, town):
    sql = """select id from Geo where name='{}' or x={} or y={}""".format(new_point["name"],
        float(new_point["x"]),
        float(new_point["y"]),)
    res = gs.SqlQuery(sql)
    if res == []:
        sql = " INSERT INTO Geo (Name, X, Y, Type, Descript, Rating, Time, town) VALUES (\'{}\', {}, {}, \'{}\', \'{}\', {}, {}, \'{}\')".format(
            new_point["name"],
            float(new_point["x"]),
            float(new_point["y"]),
            new_point["type"],
            new_point["description"],
            int(new_point["rating"]),
            int(new_point["time"]),
            town)
        gs.SqlQuery(sql)


def check_points():
    sql = """select id, x, y from geo"""
    points = gs.SqlQuery(sql)
    for i in range(len(points)):
        for j in range(i+1, len(points)):
            sql = """SELECT id FROM geo_distance where point_1={} and point_2={}""".format(
                points[i]['id'],
                points[j]['id'],)
            answer = gs.SqlQuery(sql)
            if answer == []:
                try:
                    distance = get_google([str(points[i]['x'])+','+str(points[i]['y']), str(points[j]['x'])+','+str(points[j]['y'])])
                    sql = "INSERT INTO geo_distance (point_1, point_2, distance) VALUES ({}, {}, {})".format(
                        points[i]['id'],
                        points[j]['id'],
                        distance)
                    gs.SqlQuery(sql)
                    #print(points[i]['id'], points[j]['id'])
                except:
                    logging.error(points[i]['id'], points[j]['id'], [str(points[i]['x'])+','+str(points[i]['y']), str(points[j]['x'])+','+str(points[j]['y'])])
                    pass
check_points()

"""
town = "Новосибирск"
for t in TYPES:
    google_list = get_from_google(t+"+"+town)

    for g in google_list:
        #print(g, town)
        add_new_point(g, town)
"""

