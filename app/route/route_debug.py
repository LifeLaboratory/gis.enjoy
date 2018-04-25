# coding=utf-8
from flask_restful import Resource, reqparse
from api.Log import debug_read


class Debug(Resource):
    def __init__(self):
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument('data')
        self.__parser.add_argument('arg')
        self.__args = self.__parser.parse_args()
        self.data = None
        self.filter_rec = None

    def parse_data(self):
        self.data = self.__args.get('data', None)
        self.filter_rec = self.__args.get('arg', None)

    def switch(self):
        if self.filter_rec is None:
            return debug_read()
        if self.filter_rec is not None and self.data is not None:
            answer = debug_read(self.filter_rec, self.data)
            return answer

    def get(self):
        self.parse_data()
        answer = self.switch()
        return answer, 200, {'Access-Control-Allow-Origin': '*'}
