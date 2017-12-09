# coding=utf-8
import json
from flask_restful import Resource, reqparse
from flask import request
from app.api.config import HEADER


class List(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('dict')
        args = parser.parse_args()
        print('GET /')
        print(request.headers)
        print('cookies = ', request.cookies)
        print('ARGS = ', args)
        dict = args.get('dict', None)
        answer = dict
        return answer, 200, HEADER