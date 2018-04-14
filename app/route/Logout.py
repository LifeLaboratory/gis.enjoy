# coding=utf-8
from flask_restful import Resource, reqparse
from flask import request
import api.auth.auth as auth
import api.base_name as names


class Logout(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('session')
        args = parser.parse_args()
        print('GET /')
        print(request.headers)
        print('cookies = ', request.cookies)
        print('ARGS = ', args)
        session = args.get('session')
        auth.logout_user(session)
        return {names.ANSWER: names.SUCCESS}, 200, {'Access-Control-Allow-Origin': '*'}
