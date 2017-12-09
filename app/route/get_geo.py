# coding=utf-8
from flask_restful import Resource, reqparse
from flask import request
from app.api.config import HEADER
import json
from ast import literal_eval
from app.api.get_google_dist import get_finish
from pprint import pprint

class Geo(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('origin')
        parser.add_argument('destination')
        args = parser.parse_args()
        #print('GET /')
        #print(request.headers)
        #print('cookies = ', request.cookies)
        #print('ARGS = ', args)
        origin = args.get('origin', None)
        destination = args.get('destination', None)
        data_origin = []
        data_destination = []
        data = []
        data_origin.append(literal_eval(origin)["X"])
        data_origin.append(literal_eval(origin)['Y'])
        data_destination.append(literal_eval(destination)['X'])
        data_destination.append(literal_eval(destination)['Y'])
        data_origin = tuple(data_origin)
        data_destination = tuple(data_destination)
        data = (data_origin, data_destination)
        print(data)
        answer = get_finish(data)
        pprint(answer)
        return answer, 200, HEADER

