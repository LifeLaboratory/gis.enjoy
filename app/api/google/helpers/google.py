# coding=utf-8
import requests as req
from api.helpers.service import Gis as gs
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
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&mode=walking&origins={}&destinations={}&key={}".format(
            start, finish, self.key)
        answer = s.get(url)
        answer = gs.converter(answer.text)['rows'][0]['elements'][0]['duration']['text'].split()

        if len(answer) > 2:
            if op:
                record[op] = int(answer[0]) * 60 + int(answer[2])
            return int(answer[0]) * 60 + int(answer[2])
        else:
            if op:
                record[op] = int(answer[0])
            return int(answer[0])

    def get_one_to_many(self, touch, list_touch, op=None, record=None):
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
        distance = gs.converter(self.distance)
        for i in range(len(distance["rows"][0]["elements"])):
            times = distance["rows"][0]["elements"][i]['duration']['text'].split()
            if len(times) > 2:
                result.append(int(times[0]) * 60 + int(times[2]))
            else:
                result.append(int(times[0]))
        return result

    def get_fast(self, start, finish, list_coord):
        str_destinations = ""
        for coord in list_coord:
            str_destinations += str(coord['x']) + ", " + str(coord['y']) + "|"
        str_destinations += str(finish[0]) + ", " + str(finish[1])
        str_origin = str(start[0]) + ", " + str(start[1]) + "|" + str(finish[0]) + ", " + str(finish[1])
        s = req.Session()
        for k in key:
            try:
                url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={}&destinations={}&key={}&mode=walking".format(
                    str_origin, str_destinations, k)
                answer = None
                answer = s.get(url)
                answer = gs.converter(answer.text)['rows']
                for dist in answer[0]['elements']:
                    self.record['s'].append(dist['duration']['value'] // 60)
                break
            except:
                self.key = Google.set_google_key()

        for dist in answer[0]['elements']:
            self.record['f'].append(dist['duration']['value'] // 60)
        record_o = answer[0]['elements'][len(answer[0]['elements'])-1]['duration']['value']
        self.record['s'] = self.record['s']
        self.record['f'] = self.record['f']
        self.record['o'] = record_o
        return self.record

    @staticmethod
    def set_google_key():
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=40.6655101," \
                  "-73.89188969999998&destinations=40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C" \
                  "-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C-73.9976592%7C40.6905615%2C" \
                  "-73.9976592%7C40.659569%2C-73.933783%7C40.729029%2C-73.851524%7C40.6860072%2C" \
                  "-73.6334271%7C40.598566%2C-73.7527626%7C40.659569%2C-73.933783%7C40.729029%2C" \
                  "-73.851524%7C40.6860072%2C-73.6334271%7C40.598566%2C-73.7527626&key={}"

        s = req.Session()
        for k in key:
            answer = s.get(url.format(k))
            answer = gs.converter(answer.text)
            if answer["status"] == "OK":
                return k
        return "key not found"
