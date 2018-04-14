# coding=utf-8

import api.base_name as names
from flask_restful import Resource, reqparse
from api.helpers.service import Gis as gs
from api.route import add_router, validate_router, get_router
import api.auth.auth as auth

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
        if self.data is not None:
            self.data = gs.converter(self.data)
            print("data: ", self.data)
        return


    def switch(self):
        if self.param == "add" and self.data is not None:
            answer = validate_router(self.data)
            return answer
        if self.param == "get" and self.data is None:
            answer = get_router()
            return answer
        if self.param == "get_route" and self.data is not None:
            answer = get_router(self.data)
            return answer
        if self.param == "get_usr" and self.data is not None:
            self.data[names.ID_USER] = auth.session_verification(self.data[names.UUID])
            answer = get_router(self.data[names.ID_USER])
            return answer


    def get(self):

        print("Route")
        self.parse_data()
        answer = self.switch()
        print("answer: ", answer)
        return answer, 200, {'Access-Control-Allow-Origin': '*'}
        #except:
         #   return "Error", 200, {'Access-Control-Allow-Origin': '*'}