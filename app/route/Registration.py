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
        self.data = None

    def parse_data(self):
        self.data = self.__args.get('data', None)
        self.data = gs.converter(self.data)
        print("data: ", self.data)

        return

    def check_data(self):
        if self.data[names.LOGIN] is None:
            return False
        if self.data[names.PASSWORD] is None:
            return False
        if self.data[names.NAME] is None:
            return False
        if self.data[names.EMAIL] is None:
            return False
        if self.data[names.SEX] is None:
            return False
        if self.data[names.CITY] is None:
            return False
        return True

    def switch(self):
        answer = reg.registration_user(self.data)
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