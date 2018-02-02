import requests as req
from api.helpers.json import converter
from .key import key

__author__ = 'RaldenProg'

GET_TOUCH_FROM_MANY = "https://maps.googleapis.com/maps/api/distancematrix/" \
      "json?units=metric&mode=walking&origins={}&destinations={}&key={}"


class Google:
    def __init__(self, touch, touch_list=None):
        global KEY
        self.start = str(touch[0][0]) + ',' + str(touch[0][1])
        self.end = str(touch[1][0]) + ',' + str(touch[1][1])
        self.touch_list = touch_list
        self.iter = None
        self.deep = None
        self.distance = []
        self.distance_from_start = []
        self.distance_from_end = []
        # Не уверен, что прокинется как ссылка на память (!!!)
        self.key = KEY
        self._generate_dist()

    def _generate_dist(self):
        self.distance_from_start = self._get_one_to_many(self.start)
        self.distance_from_end = self._get_one_to_many(self.end)

    def _get_one_to_many(self, touch):
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
                self.distance = req.get(GET_TOUCH_FROM_MANY.format(touch, self.touch_list, self.key)).text
            except:
                # Костыль, нужно продумать
                self.iter += 1
            break
        return self._get_distance()

    def _get_distance(self):
        result = []
        distance = converter(self.distance)
        for i in range(len(distance["rows"][0]["elements"])):
            times = distance["rows"][0]["elements"][i]['duration']['text'].split()
            if len(times) > 2:
                result.append(int(times[0]) * 60 + int(times[2]))
            else:
                result.append(int(times[0]))
        return result

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
            answer = converter(answer.text)
            if answer["status"] == "OK":
                return k
        return "key not found"
