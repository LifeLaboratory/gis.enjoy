# coding=utf-8
from flask_restful import Resource, reqparse
import api.auth.auth as auth
import api.base_name as names


class Logout(Resource):
    def __init__(self):
        self.__parser = reqparse.RequestParser()
        self.__parser.add_argument('session')
        self.__args = self.__parser.parse_args()
        self.session = None

    def parse_data(self):
        self.session = self.__args.get('session', None)

    def check_data(self):
        if self.session is None:
            return False
        return True

    def switch(self):
        auth.logout_user(self.session)

    def get(self):
        try:
            print("Registration")
            self.parse_data()
            check = self.check_data()
            if check:
                self.switch()
                return {names.ANSWER: names.SUCCESS}, 200, {'Access-Control-Allow-Origin': '*'}
            return "Error",  200, {'Access-Control-Allow-Origin': '*'}
        except:
            return "Error",  200, {'Access-Control-Allow-Origin': '*'}
