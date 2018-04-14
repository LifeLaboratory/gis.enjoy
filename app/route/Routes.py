# coding=utf-8

import api.base_name as names
from flask_restful import Resource, reqparse
from api.helpers.service import Gis as gs
from api.route import add_router, validate_router
import json

class Route(Resource):
    def __init__(self):
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument('data')
        self.__parser.add_argument('param')
        self.__args = self.__parser.parse_args()
        self.data = None

    def parse_data(self):
        self.data = self.__args.get('data', None)
        self.param = self.__args.get('param', None)
        print("param:", self.param)
        print(self.data)
        self.data = gs.converter(self.data)
        print("data: ", self.data)
        return

    def check_data(self):
        if self.data[names.UUID] is None:
            return False
        if self.data[names.NAME] is None:
            return False
        return True

    def switch(self):
        if self.param == "add" and self.data is not None:
            answer = gs.converter(validate_router(self.data))
            return answer


    def get(self):


        print("Route")
        self.parse_data()
        check = self.check_data()
        print(check)
        if check:
            answer = self.switch()
            print("answer: ", answer)
            return answer, 200, {'Access-Control-Allow-Origin': '*'}
        return "Error", 200, {'Access-Control-Allow-Origin': '*'}
        #except:
         #   return "Error", 200, {'Access-Control-Allow-Origin': '*'}