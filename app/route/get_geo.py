# coding=utf-8
from flask_restful import Resource, reqparse
from flask import request
from app.api.config import HEADER


class Geo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('param')
        parser.add_argument('page')
        args = parser.parse_args()
        print('GET /')
        print(request.headers)
        print('cookies = ', request.cookies)
        print('ARGS = ', args)
        param = args.get('param', None)
        page = args.get('page', None)
        answer = {'param': param,
                  'page': page}
        return answer, 200, HEADER

