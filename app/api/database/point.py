# encoding: utf-8
from api.helpers.service import Gis as Gs
import json
import requests as req
import logging

logging.basicConfig(filename='logger.log',
                    format='%(filename)-12s[LINE:%(lineno)d] %(levelname)-8s %(message)s %(asctime)s ',
                    level=logging.DEBUG)

TYPES = ['Парки', 'Парк', 'Сады', 'Фонтаны', 'Достопримечательности', "Монументы", 'памятники+культуры',
         'красивые+места',
         'кинотеатры', 'Природные+достопримечательности', 'храмы', 'церкви', 'театры', 'опера', 'стадионы', 'мемориалы',
         'зоопарки', 'балет', 'собор', 'галерея', 'выставка', 'сквер', 'аквапарк', 'капелла', 'цирк']


def get_google(data):
    s = req.Session()
    key = "AIzaSyDdrExQrPV2n8Y58q7EYwVgGog-6ph9LB8"
    url = """https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking
    &origins={}&destinations={}&key={}"""
    answer = s.get(url.format(data[0], data[1], key))
    answer = json.loads(answer.text)
    if answer['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
        return 999999
    answer = answer['rows'][0]['elements'][0]['duration']['text'].split()
    if len(answer) > 2:
        return int(answer[0]) * 60 + int(answer[2])
    else:
        return int(answer[0])


def add_new_point(new_point, town):
    sql = """select id from Geo where name='{}' or x={} or y={}""".format(new_point["name"],
                                                                          float(new_point["x"]),
                                                                          float(new_point["y"]), )
    res = Gs.SqlQuery(sql)
    if not res:
        sql = """INSERT INTO Geo (Name, X, Y, Type, Descript, Rating, Time, town)
              VALUES ('{}', {}, {}, '{}', '{}', {}, {}, '{}')""".format(new_point["name"],
                                                                        float(new_point["x"]),
                                                                        float(new_point["y"]),
                                                                        new_point["type"],
                                                                        new_point["description"],
                                                                        int(new_point["rating"]),
                                                                        int(new_point["time"]),
                                                                        town)
        Gs.SqlQuery(sql)


def check_points():
    sql = """select id, x, y from geo"""
    points = Gs.SqlQuery(sql)
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            sql = """SELECT id FROM geo_distance where point_1={} and point_2={}""".format(points[i]['id'],
                                                                                           points[j]['id'], )
            answer = Gs.SqlQuery(sql)
            if not answer:
                try:
                    distance = get_google([str(points[i]['x']) + ',' + str(points[i]['y']),
                                           str(points[j]['x']) + ',' + str(points[j]['y'])])
                    sql = "INSERT INTO geo_distance (point_1, point_2, distance) VALUES ({}, {}, {})".format(
                        points[i]['id'],
                        points[j]['id'],
                        distance)
                    Gs.SqlQuery(sql)
                except IndexError:
                    logging.error(points[i]['id'], points[j]['id'], [str(points[i]['x']) + ',' + str(points[i]['y']),
                                                                     str(points[j]['x']) + ',' + str(points[j]['y'])])
                    pass


check_points()
