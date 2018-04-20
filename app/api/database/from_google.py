# coding=utf8

import requests as req
from api.helpers.service import Gis as gs

def get_from_google(query):
    """
    :param query: достопримечательности+город
    :return: list с точками
    """
    key = "AIzaSyDMIfc6_9K7574xu18dG6ayTuAWsZtEOgE"
    s = req.Session()
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key={}&language=ru".format(query,
                                                                                                          key)
    answer = s.get(url)
    answer = gs.converter(answer.text)['results']
    result = []
    for res in answer:
        js = {"name": res["name"],
              "description": res["place_id"],
              "x": None,
              "y": None,
              "rating": 3,
              "time": 0}
        try:
            js["rating"] = round(res["rating"])
        except:
            js["rating"] = 0
        js["x"] = res["geometry"]["location"]["lat"]
        js["y"] = res["geometry"]["location"]["lng"]
        js["type"] = res["types"][0]
        result.append(js)
    return result
