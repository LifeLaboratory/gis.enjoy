# coding=utf-8
from flask_restful import Resource, reqparse

from app.api.get_many_google import get_many
#from config import INDEXES
from api.helpers.json import converter
from api.path import Path

class RouteGeo(Resource):
    def __init__(self):
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument('data')
        self.__args = self.__parser.parse_args()
        self.__data_origin = ()
        self.__data_destination = ()
        self.__priority = []
        self.__index_priority = []
        self.__datas = ()
        self.__time = None
        self.__data_origin_X = None
        self.__data_origin_Y = None
        self.__data_destination_X = None
        self.__data_destination_Y = None

    def parse_data(self):
        data = self.__args.get('data', None)
        data = converter(data)
        self.__data_origin_X = data["origin"]["X"]
        self.__data_origin_Y = data["origin"]['Y']
        self.__data_destination_X = data["destination"]["X"]
        self.__data_destination_Y = data["destination"]["Y"]
        self.__time = int(data["time"])
        self.__priority = data["priority"]

    def check_data(self):
        if self.__data_origin_X is None:
            return False
        if self.__data_origin_Y is None:
            return False
        if self.__data_destination_X is None:
            return False
        if self.__data_destination_Y is None:
            return False
        if self.__time is None:
            return False
        if self.__priority is None:
            return False
        return True

    def assemly_data(self):
        self.__data_origin = (float(self.__data_origin_X), float(self.__data_origin_Y))
        self.__data_destination = (float(self.__data_destination_X), float(self.__data_destination_Y))
        self.__datas = (self.__data_origin, self.__data_destination)

        #for i in range(len(self.__priority)):
        #    self.__index_priority.append(INDEXES.get(self.__priority[i], 0))

    def switch(self):
        print(self.__datas[0], self.__datas[1], self.__time, self.__index_priority)
        answer = Path(self.__datas[0], self.__datas[1], self.__time, self.__index_priority).result
        #answer = get_many(self.__datas, self.__time, self.__index_priority)
        return answer

    def get(self):
        self.parse_data()
        check = self.check_data()
        if check:
            self.assemly_data()
            answer = self.switch()
            return answer, 200, {'Access-Control-Allow-Origin': '*'}
        return "Error",  200, {'Access-Control-Allow-Origin': '*'}