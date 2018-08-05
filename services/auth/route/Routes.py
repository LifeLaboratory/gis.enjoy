# coding=utf-8
import api.base_name as names
import api.auth.auth as auth
from api.route import validate_router, get_router
from api.helpers.service import Gis as gs
from flask_restful import Resource, reqparse


class Route(Resource):
    def __init__(self):
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument('data')
        self.__parser.add_argument('param')
        self.__args = self.__parser.parse_args()
        self.data = None
        self.filter_rec = None

    def parse_data(self):
        self.data = self.__args.get('data', None)
        self.filter_rec = self.__args.get('param', None)
        if self.data is not None:
            self.data = gs.converter(self.data)

    def switch(self):
        if self.filter_rec == "add" and self.data is not None:
            answer = validate_router(self.data)
            return answer
        if self.filter_rec == "get" and self.data is None:
            answer = get_router()
            return answer
        if self.filter_rec == "get_route" and self.data is not None:
            answer = get_router(self.data)
            return answer
        if self.filter_rec == "get_usr" and self.data is not None:
            self.data[names.ID_USER] = auth.session_verification(self.data[names.UUID])
            if self.data[names.ID_USER] is None:
                return {names.ANSWER: "UUID not found"}
            answer = get_router(self.data[names.ID_USER])
            return answer

    def get(self):
        self.parse_data()
        answer = self.switch()
        return answer, 200, {'Access-Control-Allow-Origin': '*'}