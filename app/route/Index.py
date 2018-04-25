# coding=utf-8
from flask_restful import Resource
from flask import request
from config import HEADER


class Index(Resource):

    def get(self):
        print('GET /')
        print(request.headers)
        print('cookies = ', request.cookies)
        print('ARGS = ', request.args)
        return {'test': 'test'}, 200, HEADER
