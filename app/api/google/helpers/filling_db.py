__author__ = 'RaldenProg'

import requests as req
from api.helpers.json import converter
from api.sql import SqlQuery
from app.api.get_google_dist import get_google


class Filling():
    def __init__(self):
        self.key = "AIzaSyDMIfc6_9K7574xu18dG6ayTuAWsZtEOgE"
        self.result = []
    def get(self, query):
        s = req.Session()
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}&language=ru".format(query, self.key)
        answer = s.get(url)
        answer = converter(answer.text)['results']
        js = {}
        for res in answer:
            js = {"name": res["name"], "description": res["place_id"], "x": None, "y": None, "rating": 0,
                  "time": 0}
            if js["rating"]:
                js["rating"] = res["rating"]
            else:
                js["rating"] = 0
            js["x"] = res["geometry"]["location"]["lat"]
            js["y"] = res["geometry"]["location"]["lng"]
            js["type"] = res["types"][0]
            self.result.append(js)
        return self.result

    def check(self, new_point):
        sql = "SELECT * FROM Geo where x={} AND y={}".format(float(new_point["x"]), float(new_point["y"]))
        return SqlQuery(sql)

    def input_base(self, result):
        for new_point in result:
            if self.check(new_point) == []:

                sql = " INSERT INTO Geo (Name, X, Y, Type, Descript, Rating, Time) VALUES (\'{}\', {}, {}, \'{}\', \'{}\', {}, {})".format(
                    new_point["name"], float(new_point["x"]), float(new_point["y"]), new_point["type"],
                    new_point["description"], int(new_point["rating"]), int(new_point["time"]))
                print(sql)
                SqlQuery(sql)

                sql = "SELECT id FROM Geo WHERE X={} AND Y={}".format(new_point["x"], new_point["y"])
                new_point["id"] = SqlQuery(sql)
                new_point["id"] = int(new_point["id"][0]['id'])
                # print(new_point["id"][0]['id'])
                points = SqlQuery("SELECT id, x, y FROM Geo WHERE id <> (SELECT last_value from geo_id_seq)")
                for i in range(len(points)):
                    data = []
                    disti = ""
                    distj = ""
                    disti = str(points[i]['x']) + "," + str(points[i]['y'])
                    distj = str(new_point['x']) + "," + str(new_point['y'])
                    data.append(disti)
                    data.append(distj)
                    # print(data)
                    answer = get_google(data)
                    print(points[i]['id'], new_point['id'], answer)
                    sql = "INSERT INTO geo_distance (point_1, point_2, distance)" \
                          " VALUES ({}, {}, {})".format(
                        points[i]['id'],
                        new_point['id'],
                        answer)
                    # print(sql)
                    SqlQuery(sql)

                    SqlQuery("INSERT INTO geo_distance (point_1, point_2, distance)" \
                             " VALUES ({}, {}, {})".format(
                        new_point['id'],
                        points[i]['id'],
                        answer))



filling = Filling()
list = filling.get("достопримечательности+Москвы")
print(list)
print(filling.input_base(list))
