# coding=utf-8
import requests as req
from api.helpers.service import Gis
from .key import key
__author__ = 'RaldenProg'

GET_TOUCH_FROM_MANY = "https://maps.googleapis.com/maps/api/distancematrix/" \
      "json?units=metric&mode=walking&origins={}&destinations={}&key={}"


class Google:
    def __init__(self, touch=None, touch_list=None):
        self.start = str(touch[0][0]) + ',' + str(touch[0][1])
        self.end = str(touch[1][0]) + ',' + str(touch[1][1])
        self.touch_list = touch_list
        self.iter = None
        self.deep = None
        self.distance = []
        self.distance_from_start = []
        self.distance_from_end = []
        # Не уверен, что прокинется как ссылка на память (!!!)
        self.key = Google.set_google_key()
        self.record = {'s': [],
                       'f': [],
                       'o': None}

    def get_one_to_one(self, start, finish, op=None, record=None):
        start = '{},{}'.format(start[0], start[1])
        finish = '{},{}'.format(finish[0], finish[1])
        s = req.Session()
        url = """https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking&
        origins={}&destinations={}&key={}""".format(start,
                                                    finish,
                                                    self.key)
        answer = s.get(url)
        answer = Gis.converter(answer.text)['rows'][0]['elements'][0]['duration']['text'].split()

        if len(answer) > 2:
            if op:
                record[op] = int(answer[0]) * 60 + int(answer[2])
            return int(answer[0]) * 60 + int(answer[2])
        else:
            if op:
                record[op] = int(answer[0])
            return int(answer[0])

    def get_one_to_many(self, list_touch, op=None, record=None):
        text_url_touch = ""
        for point in list_touch:
            text_url_touch += str(point['x']) + "," + str(point['y']) + "%7C"
        self.iter = 0
        self.deep = 0
        while True:
            if self.iter == 3:
                self.key = Google.set_google_key()
                self.deep += 1
                self.iter = 0
            if self.deep == 3:
                raise ('ErrorKey', 'ErrorKey')
            try:
                self.distance = req.get(GET_TOUCH_FROM_MANY.format(self.start, text_url_touch, self.key)).text
            except:
                # Костыль, нужно продумать
                self.iter += 1
            break
        if op:
            record[op] = self._get_distance()
        return self._get_distance()

    def _get_distance(self):
        result = []
        distance = Gis.converter(self.distance)
        for i in range(len(distance["rows"][0]["elements"])):
            times = distance["rows"][0]["elements"][i]['duration']['text'].split()
            if len(times) > 2:
                result.append(int(times[0]) * 60 + int(times[2]))
            else:
                result.append(int(times[0]))
        return result

    def get_fast(self, start, finish, list_coord):
        str_origin = str(start[0]) + ", " + str(start[1]) + "|" + str(finish[0]) + ", " + str(finish[1])
        if len(list_coord) == 48:
            exc_range = len(list_coord) // 48 + 1
        else:
            exc_range = len(list_coord) // 48 + 2
        for i in range(1, exc_range):
            str_destinations = ""
            if i == len(list_coord) // 48 + 1:
                for j in range(48 * (i - 1), len(list_coord)):
                    str_destinations += str(list_coord[j]['x']) + ", " + str(list_coord[j]['y']) + "|"
            else:
                for j in range(48 * (i - 1), 48 * i):
                    str_destinations += str(list_coord[j]['x']) + ", " + str(list_coord[j]['y']) + "|"
            s = req.Session()
            for k in key:
                try:
                    url = """https://maps.googleapis.com/maps/api/distancematrix/json?
                    origins={}&destinations={}&key={}&mode=walking""".format(str_origin,
                                                                             str_destinations,
                                                                             k)
                    answer = None
                    answer = s.get(url)
                    answer = Gis.converter(answer.text)['rows']
                    for dist in answer[0]['elements']:
                        self.record['s'].append(dist['duration']['value'] // 60)
                    break
                except:
                    print('error')
            for dist in answer[1]['elements']:
                self.record['f'].append(dist['duration']['value'] // 60)
            record_o = answer[0]['elements'][len(answer[0]['elements']) - 1]['duration']['value']
            self.record['o'] = record_o
        return self.record

    @staticmethod
    def set_google_key():
        url = """https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking
        %20%20%20%20%20&origins=55.0606596,82.9131219&destinations=55.028232,82.908377&key={}"""
        s = req.Session()
        for k in key:
            answer = s.get(url.format(k))
            answer = Gis.converter(answer.text)
            if answer["status"] == "OK":
                return k
        return "key not found"
