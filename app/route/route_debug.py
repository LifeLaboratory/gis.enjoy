# coding=utf-8
from flask_restful import Resource, reqparse
from api.helpers.json import converter


class RouteDebug(Resource):
    def __init__(self):
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument('data')
        self.__args = self.__parser.parse_args()

    def parse_data(self):
        data = self.__args.get('data', None)
        #data = converter(data)

#    def check_data(self):


#    def assemly_data(self):


    def switch(self):
        if self.param is None:


    def get(self):
        self.parse_data()
        answer = self.switch()
        return answer, 200, {'Access-Control-Allow-Origin': '*'}
        #return "Error",  200, {'Access-Control-Allow-Origin': '*'}
