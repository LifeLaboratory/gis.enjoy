# encoding: utf-8
from api.helpers.service import Gis
from api.google.helpers.google import Google
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
    key = Google.set_google_key()
    # key = "AIzaSyCTVbmRU-8V3ya63Uce-gYTVaFugzkp794"
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
    res = Gis.SqlQuery(sql)
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
        Gis.SqlQuery(sql)


def check_points_new():
    sql = """
with
pair_point as (
 select a.id as "a_id"
  , a.x as "a_x"
  , a.y as "a_y"
  , b.id as "b_id"
  , b.x as "b_x"
  , b.y as "b_y"
 from geo a
 join geo b on a.id < b.id
 order by a.id, b.id
),
intersect_points as(
  select a.*
  from pair_point a
  left join geo_distance b on (b.point_1, b.point_2) = (a."a_id", a."b_id")
  where id is null
)
select * from intersect_points order by a_id desc, b_id
    """
    points = Gis.SqlQuery(sql)
    for point in points:
        try:
            distance = get_google([str(point['a_x']) + ',' + str(point['a_y']),
                                   str(point['b_x']) + ',' + str(point['b_y'])])
            sql = "INSERT INTO geo_distance (point_1, point_2, distance) VALUES ({}, {}, {})".format(
                            point['a_id'],
                            point['b_id'],
                            distance)
            Gis.SqlQuery(sql)
        except Exception as e:
            print(e)


def check_points():
    sql = """select id, x, y from geo"""
    points = Gis.SqlQuery(sql)
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            sql = """SELECT id FROM geo_distance where point_1={} and point_2={}""".format(points[i]['id'],
                                                                                           points[j]['id'], )
            answer = Gis.SqlQuery(sql)
            if not answer:
                try:
                    distance = get_google([str(points[i]['x']) + ',' + str(points[i]['y']),
                                           str(points[j]['x']) + ',' + str(points[j]['y'])])
                    sql = "INSERT INTO geo_distance (point_1, point_2, distance) VALUES ({}, {}, {})".format(
                        points[i]['id'],
                        points[j]['id'],
                        distance)
                    Gis.SqlQuery(sql)
                except IndexError:
                    logging.error(points[i]['id'], points[j]['id'], [str(points[i]['x']) + ',' + str(points[i]['y']),
                                                                     str(points[j]['x']) + ',' + str(points[j]['y'])])
                    pass


check_points_new()
