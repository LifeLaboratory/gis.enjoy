# coding=utf-8
import api.auth.auth as auth
from api.helpers.service import Gis as gs
from flask_restful import Resource, reqparse


class Authentication(Resource):
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
        self.data = gs.converter(self.data)

    def switch(self):
        if self.filter_rec == "get_user_name" and self.data is not None:
            self.data["id_user"] = auth.session_verification(self.data["UUID"])
            answer = gs.converter(auth.get_user_name(self.data["id_user"]))
        else:
            answer = gs.converter(gs.converter(auth.login_verification(self.data)))
        return answer

    def get(self):
        try:
            self.parse_data()
            answer = self.switch()
            return answer, 200, {'Access-Control-Allow-Origin': '*'}
        except:
            return "Error", 200, {'Access-Control-Allow-Origin': '*'}
