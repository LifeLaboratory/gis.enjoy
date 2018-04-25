# coding=utf-8
from flask_restful import Resource, reqparse
import api.auth.registration_users as reg
import api.base_name as names
from api.helpers.service import Gis as gs


class Registration(Resource):
    def __init__(self):
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument('data')
        self.__args = self.__parser.parse_args()
        self.filter_rec = None

    def parse_data(self):
        self.filter_rec = self.__args.get('data', None)
        self.filter_rec = gs.converter(self.filter_rec)

    def check_data(self):
        if self.filter_rec[names.LOGIN] is None:
            return False
        if self.filter_rec[names.PASSWORD] is None:
            return False
        if self.filter_rec[names.NAME] is None:
            return False
        if self.filter_rec[names.EMAIL] is None:
            return False
        if self.filter_rec[names.SEX] is None:
            return False
        if self.filter_rec[names.CITY] is None:
            return False
        return True

    def switch(self):
        answer = reg.registration_user(self.filter_rec)
        return answer

    def get(self):
        try:
            print("Registration")
            self.parse_data()
            check = self.check_data()
            if check:
                answer = self.switch()
                print("answer: ", answer)
                return answer, 200, {'Access-Control-Allow-Origin': '*'}
            return "Error",  200, {'Access-Control-Allow-Origin': '*'}
        except:
            return "Error",  200, {'Access-Control-Allow-Origin': '*'}