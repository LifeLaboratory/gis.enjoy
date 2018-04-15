# coding=utf-8
from flask_restful import Resource, reqparse
from api.helpers.service import Gis as gs
from api.Log import debug_read

class Debug(Resource):
    def __init__(self):
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument('data')
        self.__parser.add_argument('arg')
        self.__args = self.__parser.parse_args()
        self.data = None
        self.arg = None

    def parse_data(self):
        self.data = self.__args.get('data', None)
        self.arg = self.__args.get('arg', None)
        print("arg: ", self.arg)
        print("data: ", self.data)

    def switch(self):
        if self.arg is None:
            return debug_read()
        if self.arg is not None and self.data is not None:
            answer = debug_read(self.arg, self.data)
            print(answer)
            return answer



    def get(self):
        self.parse_data()
        answer = self.switch()
        return answer, 200, {'Access-Control-Allow-Origin': '*'}
        #return "Error",  200, {'Access-Control-Allow-Origin': '*'}
